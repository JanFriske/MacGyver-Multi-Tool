import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.translation_validator import get_validator
from core.services.user_override_service import get_override_service

def test_import_export():
    print("Testing Import/Export Validation...")
    validator = get_validator()
    service = get_override_service()
    
    # Test Data
    lang = "de"
    key = "menu.file"
    value = "Datei (Importiert)"
    
    # 1. Create Valid Import Data
    valid_data = {
        "export_format": "macgyver_translation_single",
        "version": "1.0",
        "author": "Test User",
        "language": lang,
        "translations": {
            key: value
        }
    }
    
    valid_file = Path("tests/temp_valid_import.json")
    with open(valid_file, 'w', encoding='utf-8') as f:
        json.dump(valid_data, f)
        
    print(f"1. Created valid import file: {valid_file}")
    
    # 2. Validate File
    print("2. Validating file...")
    valid, msg, sanitized_data = validator.validate_import_file(valid_file)
    
    if valid:
        print("   ✅ Validation passed")
    else:
        print(f"   ❌ Validation failed: {msg}")
        return

    # 3. Import Data
    print("3. Importing data...")
    # Simulate what TranslationEditorDialog._import_single_language does
    translations = sanitized_data.get('translations', {})
    for k, v in translations.items():
        service.save_override(lang, k, v)
        
    # Verify
    loaded_value = service.get_override(lang, key)
    if loaded_value == value:
        print(f"   ✅ Import verified: {lang}.{key} = {loaded_value}")
    else:
        print(f"   ❌ Import failed: Expected '{value}', got '{loaded_value}'")

    # 4. Test Invalid Data (Missing Author)
    print("4. Testing invalid data (missing author)...")
    invalid_data = valid_data.copy()
    del invalid_data["author"]
    
    invalid_file = Path("tests/temp_invalid_import.json")
    with open(invalid_file, 'w', encoding='utf-8') as f:
        json.dump(invalid_data, f)
        
    valid, msg, _ = validator.validate_import_file(invalid_file)
    
    if not valid and "author" in msg.lower():
        print(f"   ✅ Validation correctly failed: {msg}")
    else:
        print(f"   ❌ Validation should have failed for missing author. Result: {valid}, Msg: {msg}")

    # Cleanup
    if valid_file.exists(): valid_file.unlink()
    if invalid_file.exists(): invalid_file.unlink()
    service.remove_override(lang, key)

if __name__ == "__main__":
    test_import_export()
