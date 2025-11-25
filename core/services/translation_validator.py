"""
Translation Import/Export Validation
Provides security validation and author attribution enforcement for translation files
"""
import json
import re
from typing import Dict, Tuple, Optional
from pathlib import Path

class TranslationValidator:
    """Validates translation import/export files"""
    
    # Maximum file size: 10 MB
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Maximum translation value length
    MAX_VALUE_LENGTH = 500
    
    # Allowed export formats
    ALLOWED_FORMATS = [
        "macgyver_translation_single",
        "macgyver_translation_multi",
        "macgyver_translation_custom"
    ]
    
    def __init__(self, master_db_path: Optional[Path] = None):
        self.master_db_path = master_db_path or Path("i18n/translation_master.json")
        self.valid_keys = self._load_valid_keys()
    
    def _load_valid_keys(self) -> set:
        """Load valid translation keys from master DB"""
        if not self.master_db_path.exists():
            # Fallback to en.json
            en_file = Path("i18n/translations/en.json")
            if en_file.exists():
                with open(en_file, 'r', encoding='utf-8') as f:
                    en_data = json.load(f)
                    return set(self._flatten_keys(en_data))
            return set()
        
        with open(self.master_db_path, 'r', encoding='utf-8') as f:
            master_data = json.load(f)
            return set(master_data['translations'].keys())
    
    def _flatten_keys(self, d, parent=''):
        """Flatten nested dict keys"""
        keys = []
        for k, v in d.items():
            full_key = f"{parent}.{k}" if parent else k
            if isinstance(v, dict):
                keys.extend(self._flatten_keys(v, full_key))
            else:
                keys.append(full_key)
        return keys
    
    def validate_file_size(self, file_path: Path) -> Tuple[bool, str]:
        """Validate file size"""
        if not file_path.exists():
            return False, "File does not exist"
        
        size = file_path.stat().st_size
        if size > self.MAX_FILE_SIZE:
            return False, f"File too large: {size / (1024*1024):.1f} MB (max: 10 MB)"
        
        return True, "OK"
    
    def validate_json_structure(self, data: Dict) -> Tuple[bool, str]:
        """Validate basic JSON structure"""
        # Check required fields
        if "export_format" not in data:
            return False, "Missing required field: export_format"
        
        if data["export_format"] not in self.ALLOWED_FORMATS:
            return False, f"Invalid export format: {data['export_format']}"
        
        if "version" not in data:
            return False, "Missing required field: version"
        
        # MANDATORY: Check for author field
        if "author" not in data:
            return False, "Missing MANDATORY field: author (author attribution is required)"
        
        author = data.get("author", "").strip()
        if not author:
            return False, "Author field cannot be empty (author attribution is MANDATORY)"
        
        return True, "OK"
    
    def validate_translation_keys(self, translations: Dict) -> Tuple[bool, str, list]:
        """Validate translation keys against whitelist"""
        invalid_keys = []
        
        for key in translations.keys():
            if key not in self.valid_keys:
                invalid_keys.append(key)
        
        if invalid_keys:
            return False, f"Found {len(invalid_keys)} invalid/unknown keys", invalid_keys[:10]
        
        return True, "All keys valid", []
    
    def sanitize_translation_value(self, value: str) -> Tuple[str, bool]:
        """Sanitize translation value"""
        if not isinstance(value, str):
            return str(value), True
        
        # Check length
        if len(value) > self.MAX_VALUE_LENGTH:
            return value[:self.MAX_VALUE_LENGTH], True
        
        # Remove control characters (except newline and tab)
        sanitized = ''.join(c for c in value if c.isprintable() or c in '\n\t')
        
        # Check for potential injection attempts
        dangerous_patterns = [
            r'\.\./+',  # Path traversal
            r'%APPDATA%',  # Environment variables
            r'<script',  # HTML injection
            r'javascript:',  # JS injection
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return "", True  # Empty value if dangerous pattern found
        
        was_modified = (sanitized != value)
        return sanitized, was_modified
    
    def validate_language_code(self, lang_code: str) -> Tuple[bool, str]:
        """Validate language code format"""
        # Allow alphanumeric and underscore only
        if not re.match(r'^[a-z0-9_]+$', lang_code):
            return False, f"Invalid language code format: {lang_code}"
        
        # Check length
        if len(lang_code) > 50:
            return False, "Language code too long (max: 50 characters)"
        
        return True, "OK"
    
    def validate_import_file(self, file_path: Path) -> Tuple[bool, str, Optional[Dict]]:
        """Complete validation of import file"""
        # 1. File size
        valid, msg = self.validate_file_size(file_path)
        if not valid:
            return False, msg, None
        
        # 2. Load JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}", None
        except UnicodeDecodeError:
            return False, "File encoding error (must be UTF-8)", None
        except Exception as e:
            return False, f"Failed to read file: {str(e)}", None
        
        # 3. Structure validation
        valid, msg = self.validate_json_structure(data)
        if not valid:
            return False, msg, None
        
        # 4. Format-specific validation
        export_format = data["export_format"]
        
        if export_format == "macgyver_translation_single":
            valid, msg = self._validate_single_format(data)
        elif export_format == "macgyver_translation_multi":
            valid, msg = self._validate_multi_format(data)
        elif export_format == "macgyver_translation_custom":
            valid, msg = self._validate_custom_format(data)
        else:
            return False, f"Unsupported format: {export_format}", None
        
        if not valid:
            return False, msg, None
        
        # 5. Sanitize all values
        sanitized_data = self._sanitize_data(data)
        
        return True, "Validation successful", sanitized_data
    
    def _validate_single_format(self, data: Dict) -> Tuple[bool, str]:
        """Validate single language format"""
        if "language" not in data:
            return False, "Missing field: language"
        
        if "translations" not in data:
            return False, "Missing field: translations"
        
        # Validate language code
        valid, msg = self.validate_language_code(data["language"])
        if not valid:
            return False, msg
        
        # Validate keys
        valid, msg, invalid_keys = self.validate_translation_keys(data["translations"])
        if not valid:
            return False, f"{msg}. First invalid keys: {', '.join(invalid_keys)}"
        
        return True, "OK"
    
    def _validate_multi_format(self, data: Dict) -> Tuple[bool, str]:
        """Validate multi language format"""
        if "languages" not in data:
            return False, "Missing field: languages"
        
        languages = data["languages"]
        if not isinstance(languages, dict):
            return False, "Field 'languages' must be a dictionary"
        
        for lang_code, lang_data in languages.items():
            # Validate language code
            valid, msg = self.validate_language_code(lang_code)
            if not valid:
                return False, f"Language '{lang_code}': {msg}"
            
            # Validate translations
            if "translations" not in lang_data:
                return False, f"Language '{lang_code}': missing translations"
            
            valid, msg, invalid_keys = self.validate_translation_keys(lang_data["translations"])
            if not valid:
                return False, f"Language '{lang_code}': {msg}"
        
        return True, "OK"
    
    def _validate_custom_format(self, data: Dict) -> Tuple[bool, str]:
        """Validate custom language format"""
        required_fields = ["language_code", "language_name", "translations"]
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate language code
        lang_code = data["language_code"]
        if not lang_code.startswith("custom_"):
            return False, "Custom language code must start with 'custom_'"
        
        valid, msg = self.validate_language_code(lang_code)
        if not valid:
            return False, msg
        
        return True, "OK"
    
    def _sanitize_data(self, data: Dict) -> Dict:
        """Sanitize all translation values in data"""
        sanitized = data.copy()
        
        export_format = data["export_format"]
        
        if export_format == "macgyver_translation_single":
            sanitized["translations"] = self._sanitize_translations(data["translations"])
        elif export_format == "macgyver_translation_multi":
            sanitized["languages"] = {}
            for lang_code, lang_data in data["languages"].items():
                sanitized["languages"][lang_code] = {
                    "language_name": lang_data.get("language_name", ""),
                    "translations": self._sanitize_translations(lang_data.get("translations", {}))
                }
        elif export_format == "macgyver_translation_custom":
            sanitized["translations"] = self._sanitize_translations(data.get("translations", {}))
        
        return sanitized
    
    def _sanitize_translations(self, translations: Dict) -> Dict:
        """Sanitize all values in translations dict"""
        sanitized = {}
        for key, value in translations.items():
            if isinstance(value, dict):
                sanitized[key] = self._sanitize_translations(value)
            else:
                sanitized[key], _ = self.sanitize_translation_value(value)
        return sanitized

# Global validator instance
_validator = None

def get_validator() -> TranslationValidator:
    """Get or create global validator instance"""
    global _validator
    if _validator is None:
        _validator = TranslationValidator()
    return _validator
