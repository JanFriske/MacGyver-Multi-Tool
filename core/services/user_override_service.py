"""
User Override Service
Manages user-specific translation overrides stored in AppData
MSIX-compatible storage location
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

class UserOverrideService:
    """Manages user translation overrides in AppData"""
    
    def __init__(self):
        self.user_data_dir = self._get_user_data_dir()
        self.overrides_file = self.user_data_dir / "user_translations" / "overrides.json"
        self.overrides: Dict[str, Dict[str, str]] = {}
        self._load_overrides()
    
    def _get_user_data_dir(self) -> Path:
        """Get MSIX-compatible user data directory"""
        if os.name == 'nt':  # Windows
            appdata = Path(os.getenv('LOCALAPPDATA'))
            
            # Check if running in MSIX container
            package_path = appdata / "Packages" / "JanFriske.MacGyverMulti-Tool_34mw99vg9ewf2" / "LocalCache" / "Local"
            
            if package_path.parent.parent.exists():
                # In MSIX container
                user_dir = package_path
            else:
                # Development mode (not packaged)
                user_dir = appdata / "JanFriske" / "MacGyverMultiTool"
        else:  # Linux/Mac (future)
            user_dir = Path.home() / ".config" / "MacGyverMultiTool"
        
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def _load_overrides(self):
        """Load user overrides from AppData"""
        if not self.overrides_file.exists():
            print("[UserOverrides] No existing overrides found")
            return
        
        try:
            with open(self.overrides_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.overrides = data.get("overrides", {})
                print(f"[UserOverrides] Loaded {len(self.overrides)} language overrides")
        except Exception as e:
            print(f"[UserOverrides] Error loading overrides: {e}")
            self.overrides = {}
    
    def _persist_overrides(self):
        """Save overrides to AppData"""
        # Ensure directory exists
        self.overrides_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "user_id": "local",
            "created": self._get_creation_time(),
            "last_modified": datetime.now().isoformat(),
            "overrides": self.overrides
        }
        
        try:
            with open(self.overrides_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[UserOverrides] Saved to: {self.overrides_file}")
        except Exception as e:
            print(f"[UserOverrides] Error saving overrides: {e}")
    
    def _get_creation_time(self) -> str:
        """Get creation time or use current time"""
        if self.overrides_file.exists():
            try:
                with open(self.overrides_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("created", datetime.now().isoformat())
            except:
                pass
        return datetime.now().isoformat()
    
    def save_override(self, lang_code: str, key: str, value: str):
        """Save a translation override for a specific language"""
        if lang_code not in self.overrides:
            self.overrides[lang_code] = {}
        
        # Flatten the key if it's dot-notation
        self.overrides[lang_code][key] = value
        self._persist_overrides()
        print(f"[UserOverrides] Saved: {lang_code}.{key} = {value}")
    
    def remove_override(self, lang_code: str, key: str):
        """Remove a translation override"""
        if lang_code in self.overrides:
            if key in self.overrides[lang_code]:
                del self.overrides[lang_code][key]
                self._persist_overrides()
                print(f"[UserOverrides] Removed: {lang_code}.{key}")
    
    def get_override(self, lang_code: str, key: str) -> Optional[str]:
        """Get a translation override if it exists"""
        return self.overrides.get(lang_code, {}).get(key)
    
    def get_all_overrides(self, lang_code: str) -> Dict[str, str]:
        """Get all overrides for a language"""
        return self.overrides.get(lang_code, {}).copy()
    
    def clear_language_overrides(self, lang_code: str):
        """Clear all overrides for a language"""
        if lang_code in self.overrides:
            del self.overrides[lang_code]
            self._persist_overrides()
            print(f"[UserOverrides] Cleared all overrides for: {lang_code}")
    
    def get_override_count(self, lang_code: str) -> int:
        """Get count of overrides for a language"""
        return len(self.overrides.get(lang_code, {}))
    
    def export_overrides(self, lang_code: str) -> Dict:
        """Export overrides for a language (for sharing)"""
        return {
            "language": lang_code,
            "translations": self.get_all_overrides(lang_code),
            "exported_at": datetime.now().isoformat()
        }
    
    def import_overrides(self, lang_code: str, translations: Dict[str, str], merge: bool = True):
        """Import overrides for a language"""
        if merge:
            # Merge with existing
            if lang_code not in self.overrides:
                self.overrides[lang_code] = {}
            self.overrides[lang_code].update(translations)
        else:
            # Replace all
            self.overrides[lang_code] = translations.copy()
        
        self._persist_overrides()
        print(f"[UserOverrides] Imported {len(translations)} overrides for: {lang_code}")

# Global instance
_override_service = None

def get_override_service() -> UserOverrideService:
    """Get or create the global override service instance"""
    global _override_service
    if _override_service is None:
        _override_service = UserOverrideService()
    return _override_service
