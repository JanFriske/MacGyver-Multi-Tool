"""
Fix Language Files
Adds missing structural keys (menu_file, menu_edit, etc.) to incomplete language files.
Uses de.json as template for structure.
"""
import json
import os
from pathlib import Path
import shutil

def fix_languages():
    base_path = Path("i18n/translations")
    template_file = base_path / "de.json"
    
    # Load template
    with open(template_file, 'r', encoding='utf-8') as f:
        template_data = json.load(f)
        
    # Keys to enforce
    structural_keys = [
        "menu_file", 
        "menu_edit", 
        "menu_view", 
        "menu_tools"
    ]
    
    files = list(base_path.glob("*.json"))
    fixed_count = 0
    
    print(f"🔧 Fixing language files using template: {template_file.name}")
    
    for file_path in files:
        if file_path.name in ["de.json", "en.json", "de_middlehigh.json"]:
            continue # Skip reference files
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            # Check and add missing keys
            for key in structural_keys:
                if key not in data:
                    print(f"  [{file_path.stem}] Adding missing key: {key}")
                    # Copy from template (Standard German fallback)
                    # Ideally we would use English for non-German languages,
                    # but structure is priority now.
                    data[key] = template_data[key]
                    modified = True
            
            if modified:
                # Save back
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ Error fixing {file_path.name}: {e}")

    print(f"\n✅ Fixed {fixed_count} files.")

if __name__ == "__main__":
    os.chdir("c:/Dev/Repos/JanFriske/MacGyver Multi-Tool")
    fix_languages()
