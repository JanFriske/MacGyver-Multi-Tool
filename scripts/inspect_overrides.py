"""
Inspect user overrides file for emojis
"""
import os
import json
from pathlib import Path

def get_user_data_dir():
    if os.name == 'nt':
        appdata = Path(os.getenv('LOCALAPPDATA'))
        # Check if running in MSIX container
        package_path = appdata / "Packages" / "JanFriske.MacGyverMulti-Tool_34mw99vg9ewf2" / "LocalCache" / "Local"
        
        if package_path.parent.parent.exists():
            return package_path
        else:
            return appdata / "JanFriske" / "MacGyverMultiTool"
    return Path.home() / ".config" / "MacGyverMultiTool"

user_dir = get_user_data_dir()
overrides_file = user_dir / "user_translations" / "overrides.json"

print(f"Checking overrides file: {overrides_file}")

if overrides_file.exists():
    try:
        with open(overrides_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print("Content:")
            print(content)
            
            # Check for emojis
            data = json.loads(content)
            overrides = data.get("overrides", {})
            found_emojis = False
            for lang, trans in overrides.items():
                for key, val in trans.items():
                    if any(ord(c) > 127 for c in val):
                        print(f"⚠️ FOUND EMOJI/SPECIAL CHAR in {lang}.{key}: {val}")
                        found_emojis = True
            
            if not found_emojis:
                print("✅ No emojis found in overrides.")
                
    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print("File does not exist.")
