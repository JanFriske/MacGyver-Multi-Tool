"""
Custom Language Service
Manages user-created custom languages stored in AppData
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

class CustomLanguageService:
    """Manages custom user-created languages"""
    
    def __init__(self):
        self.user_data_dir = self._get_user_data_dir()
        self.custom_dir = self.user_data_dir / "custom_languages"
        self.custom_dir.mkdir(parents=True, exist_ok=True)
        self.custom_languages: Dict[str, Dict] = {}
        self._load_custom_languages()
    
    def _get_user_data_dir(self) -> Path:
        """Get MSIX-compatible user data directory"""
        if os.name == 'nt':
            appdata = Path(os.getenv('LOCALAPPDATA'))
            package_path = appdata / "Packages" / "JanFriske.MacGyverMulti-Tool_34mw99vg9ewf2" / "LocalCache" / "Local"
            
            if package_path.parent.parent.exists():
                user_dir = package_path
            else:
                user_dir = appdata / "JanFriske" / "MacGyverMultiTool"
        else:
            user_dir = Path.home() / ".config" / "MacGyverMultiTool"
        
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def _load_custom_languages(self):
        """Load all custom languages from AppData"""
        if not self.custom_dir.exists():
            return
        
        for lang_file in self.custom_dir.glob("custom_*.json"):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)
                    lang_code = lang_data.get("language_code")
                    if lang_code:
                        self.custom_languages[lang_code] = lang_data
                        print(f"[CustomLanguages] Loaded: {lang_code}")
            except Exception as e:
                print(f"[CustomLanguages] Error loading {lang_file}: {e}")
    
    def create_custom_language(self, name: str, code: str, description: str = "", 
                              base_language: str = "en", author: str = "User") -> bool:
        """Create a new custom language"""
        # Ensure code has custom_ prefix
        if not code.startswith("custom_"):
            code = f"custom_{code}"
        
        # Sanitize code (alphanumeric and underscore only)
        code = ''.join(c for c in code if c.isalnum() or c == '_')
        
        # Check if already exists
        if code in self.custom_languages:
            raise ValueError(f"Custom language '{code}' already exists")
        
        # Load base translations
        base_translations = self._get_base_translations(base_language)
        
        # Create custom language data
        lang_data = {
            "language_code": code,
            "language_name": name,
            "description": description,
            "base_language": base_language,
            "created_at": datetime.now().isoformat(),
            "created_by": author,
            "is_custom": True,
            "translations": base_translations
        }
        
        # Save to file
        lang_file = self.custom_dir / f"{code}.json"
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, indent=2, ensure_ascii=False)
        
        # Load into memory
        self.custom_languages[code] = lang_data
        print(f"[CustomLanguages] Created: {code} ({name})")
        
        return True
    
    def _get_base_translations(self, base_lang: str) -> Dict:
        """Get base translations from a language file"""
        lang_file = Path("i18n/translations") / f"{base_lang}.json"
        
        if lang_file.exists():
            with open(lang_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    
    def delete_custom_language(self, code: str) -> bool:
        """Delete a custom language"""
        if not code.startswith("custom_"):
            raise ValueError("Only custom languages can be deleted")
        
        if code not in self.custom_languages:
            return False
        
        # Delete file
        lang_file = self.custom_dir / f"{code}.json"
        if lang_file.exists():
            lang_file.unlink()
        
        # Remove from memory
        del self.custom_languages[code]
        print(f"[CustomLanguages] Deleted: {code}")
        
        return True
    
    def get_custom_language(self, code: str) -> Optional[Dict]:
        """Get a custom language by code"""
        return self.custom_languages.get(code)
    
    def get_all_custom_languages(self) -> Dict[str, Dict]:
        """Get all custom languages"""
        return self.custom_languages.copy()
    
    def get_custom_language_codes(self) -> List[str]:
        """Get list of all custom language codes"""
        return list(self.custom_languages.keys())
    
    def update_custom_translation(self, lang_code: str, key: str, value: str):
        """Update a translation in a custom language"""
        if lang_code not in self.custom_languages:
            raise ValueError(f"Custom language '{lang_code}' not found")
        
        # Update in nested structure
        lang_data = self.custom_languages[lang_code]
        keys = key.split('.')
        current = lang_data["translations"]
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        
        # Save to file
        lang_file = self.custom_dir / f"{lang_code}.json"
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, indent=2, ensure_ascii=False)
            
    def remove_custom_translation(self, lang_code: str, key: str):
        """Remove a translation from a custom language (revert to base)"""
        if lang_code not in self.custom_languages:
            raise ValueError(f"Custom language '{lang_code}' not found")
        
        # Update in nested structure
        lang_data = self.custom_languages[lang_code]
        keys = key.split('.')
        current = lang_data["translations"]
        
        # Navigate to parent of the key
        parent = current
        for k in keys[:-1]:
            if k not in parent:
                return # Key doesn't exist, nothing to remove
            parent = parent[k]
        
        # Remove key if exists
        if keys[-1] in parent:
            del parent[keys[-1]]
            
            # Save to file
            lang_file = self.custom_dir / f"{lang_code}.json"
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(lang_data, f, indent=2, ensure_ascii=False)
    
    def export_custom_language(self, lang_code: str) -> Dict:
        """Export a custom language for sharing"""
        if lang_code not in self.custom_languages:
            raise ValueError(f"Custom language '{lang_code}' not found")
        
        lang_data = self.custom_languages[lang_code]
        
        # Flatten translations for export
        flat_translations = self._flatten_dict(lang_data["translations"])
        
        return {
            "export_format": "macgyver_translation_custom",
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "language_code": lang_code,
            "language_name": lang_data["language_name"],
            "description": lang_data.get("description", ""),
            "base_language": lang_data["base_language"],
            "is_custom": True,
            "author": lang_data.get("created_by", "Unknown"),
            "translations": flat_translations,
            "metadata": {
                "total_translations": len(flat_translations),
                "created_at": lang_data.get("created_at", "")
            }
        }
    
    def import_custom_language(self, data: Dict) -> str:
        """Import a custom language from export data"""
        lang_code = data.get("language_code")
        lang_name = data.get("language_name")
        
        if not lang_code or not lang_code.startswith("custom_"):
            raise ValueError("Invalid custom language code")
        
        # Check if already exists
        if lang_code in self.custom_languages:
            # Offer to overwrite or rename
            raise FileExistsError(f"Custom language '{lang_code}' already exists")
        
        # Create from import data
        translations = data.get("translations", {})
        nested_translations = self._unflatten_dict(translations)
        
        lang_data = {
            "language_code": lang_code,
            "language_name": lang_name,
            "description": data.get("description", ""),
            "base_language": data.get("base_language", "en"),
            "created_at": data.get("metadata", {}).get("created_at", datetime.now().isoformat()),
            "created_by": data.get("author", "Imported"),
            "is_custom": True,
            "translations": nested_translations
        }
        
        # Save
        lang_file = self.custom_dir / f"{lang_code}.json"
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, indent=2, ensure_ascii=False)
        
        self.custom_languages[lang_code] = lang_data
        print(f"[CustomLanguages] Imported: {lang_code}")
        
        return lang_code
    
    def _flatten_dict(self, d, parent=''):
        """Flatten nested dict to dot notation"""
        items = {}
        for k, v in d.items():
            full_key = f"{parent}.{k}" if parent else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, full_key))
            else:
                items[full_key] = v
        return items
    
    def _unflatten_dict(self, flat_dict):
        """Convert flat dict to nested structure"""
        result = {}
        for key, value in flat_dict.items():
            parts = key.split('.')
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

# Global instance
_custom_language_service = None

def get_custom_language_service() -> CustomLanguageService:
    """Get or create global custom language service"""
    global _custom_language_service
    if _custom_language_service is None:
        _custom_language_service = CustomLanguageService()
    return _custom_language_service
