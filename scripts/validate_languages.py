"""
Validate Language Files
Checks all JSON files in i18n/translations for:
1. Valid JSON syntax
2. Presence of critical keys (menu_file, etc.)
3. File structure consistency
"""
import json
import os
from pathlib import Path

def validate_languages():
    base_path = Path("i18n/translations")
    files = list(base_path.glob("*.json"))
    
    print(f"🔍 Scanning {len(files)} language files...\n")
    
    corrupt_files = []
    incomplete_files = []
    valid_files = []
    
    critical_keys = [
        "menu", 
        "menu_file", 
        "menu_edit", 
        "menu_view", 
        "menu_tools",
        "widgets",
        "dialogs"
    ]
    
    for file_path in files:
        lang_code = file_path.stem
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check structure
            missing_keys = []
            for key in critical_keys:
                if key not in data:
                    missing_keys.append(key)
            
            if missing_keys:
                incomplete_files.append((lang_code, missing_keys))
                print(f"⚠️  {lang_code}: Valid JSON, but missing keys: {missing_keys}")
            else:
                valid_files.append(lang_code)
                # print(f"✅ {lang_code}: OK")
                
        except json.JSONDecodeError as e:
            corrupt_files.append((lang_code, str(e)))
            print(f"❌ {lang_code}: CORRUPT JSON! {e}")
        except Exception as e:
            print(f"❌ {lang_code}: Error reading file: {e}")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Valid Files:      {len(valid_files)}")
    print(f"⚠️  Incomplete Files: {len(incomplete_files)}")
    print(f"❌ Corrupt Files:    {len(corrupt_files)}")
    
    if corrupt_files:
        print("\nCORRUPT FILES (Must be fixed/deleted):")
        for code, err in corrupt_files:
            print(f"  - {code}: {err}")
            
    if incomplete_files:
        print("\nINCOMPLETE FILES (Need structure update):")
        for code, keys in incomplete_files:
            print(f"  - {code}: Missing {len(keys)} keys")

if __name__ == "__main__":
    os.chdir("c:/Dev/Repos/JanFriske/MacGyver Multi-Tool")
    validate_languages()
