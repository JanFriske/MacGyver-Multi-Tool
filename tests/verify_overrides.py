import sys
import os
from pathlib import Path
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.user_override_service import get_override_service

def test_override_persistence():
    print("Testing User Override Persistence...")
    service = get_override_service()
    
    # Test Data
    lang = "de"
    key = "test.key"
    value = "Test Wert"
    
    # 1. Save Override
    print(f"1. Saving override: {lang}.{key} = {value}")
    service.save_override(lang, key, value)
    
    # Verify in memory
    loaded_value = service.get_override(lang, key)
    if loaded_value == value:
        print("   ✅ In-memory verification passed")
    else:
        print(f"   ❌ In-memory verification failed: Expected '{value}', got '{loaded_value}'")
        return

    # 2. Verify File Persistence
    user_dir = service._get_user_data_dir()
    overrides_file = user_dir / "user_translations" / "overrides.json"
    
    if overrides_file.exists():
        print(f"   ✅ File exists: {overrides_file}")
        try:
            with open(overrides_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                file_value = data.get("overrides", {}).get(lang, {}).get(key)
                if file_value == value:
                    print("   ✅ File content verification passed")
                else:
                    print(f"   ❌ File content verification failed: Expected '{value}', got '{file_value}'")
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    else:
        print(f"   ❌ File does not exist: {overrides_file}")
        return

    # 3. Remove Override
    print(f"3. Removing override: {lang}.{key}")
    service.remove_override(lang, key)
    
    # Verify removal in memory
    loaded_value = service.get_override(lang, key)
    if loaded_value is None:
        print("   ✅ In-memory removal verification passed")
    else:
        print(f"   ❌ In-memory removal verification failed: Got '{loaded_value}'")

    # Verify removal in file
    with open(overrides_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        file_value = data.get("overrides", {}).get(lang, {}).get(key)
        if file_value is None:
            print("   ✅ File removal verification passed")
        else:
            print(f"   ❌ File removal verification failed: Got '{file_value}'")

if __name__ == "__main__":
    test_override_persistence()
