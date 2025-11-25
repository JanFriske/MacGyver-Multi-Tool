#!/usr/bin/env python3
"""
Fill Missing Translation Keys
Supports two modes:
  - Legacy: Use en.json as fallback (default)
  - Master: Generate from translation_master.json
"""
import json
import argparse
from pathlib import Path

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def unflatten_dict(flat_dict):
    """Convert flat dict back to nested structure"""
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

def fill_missing_keys_legacy():
    """Legacy mode: Use en.json as fallback"""
    base_path = Path("i18n/translations")
    en_file = base_path / "en.json"
    
    print(f"🔧 [LEGACY MODE] Filling missing keys using fallback: {en_file.name}\n")
    
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    files = list(base_path.glob("*.json"))
    fixed_count = 0
    
    for file_path in files:
        if file_path.name == "en.json":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            def ensure_keys(target_dict, source_dict):
                nonlocal modified
                for k, v in source_dict.items():
                    if k not in target_dict:
                        target_dict[k] = v
                        print(f"  [{file_path.stem}] Added missing key: {k}")
                        modified = True
                    elif isinstance(v, dict):
                        if not isinstance(target_dict[k], dict):
                            target_dict[k] = v
                            modified = True
                        else:
                            ensure_keys(target_dict[k], v)
            
            ensure_keys(data, en_data)
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ Error fixing {file_path.name}: {e}")

    print(f"\n✅ Fixed {fixed_count} language files.")

def fill_missing_keys_master(validate_only=False):
    """Master mode: Generate from translation_master.json"""
    master_file = Path("i18n/translation_master.json")
    translations_dir = Path("i18n/translations")
    
    if not master_file.exists():
        print(f"❌ Master database not found: {master_file}")
        print(f"   Run create_master_db.py first!")
        return
    
    print(f"🔧 [MASTER MODE] Generating/updating from: {master_file.name}\n")
    
    # Load master database
    with open(master_file, 'r', encoding='utf-8') as f:
        master_db = json.load(f)
    
    translations = master_db['translations']
    supported_languages = set(master_db['metadata']['supported_languages'])
    
    # Get all language codes that have at least one translation
    all_lang_codes = set()
    for trans in translations.values():
        all_lang_codes.update(trans['values'].keys())
    
    print(f"   Master DB: {len(translations)} keys")
    print(f"   Languages in DB: {len(all_lang_codes)}")
    print(f"   Generating for: {sorted(all_lang_codes)}\n")
    
    if validate_only:
        print("✅ Validation mode - no files will be modified\n")
    
    generated_count = 0
    updated_count = 0
    
    for lang_code in sorted(all_lang_codes):
        lang_file = translations_dir / f"{lang_code}.json"
        
        # Build flat translations for this language
        flat_trans = {}
        for key, data in translations.items():
            # Priority: specific language > English fallback
            value = data['values'].get(lang_code, data['values'].get('en', ''))
            flat_trans[key] = value
        
        # Convert to nested structure
        nested_trans = unflatten_dict(flat_trans)
        
        if validate_only:
            # Just check if file exists and is valid
            if lang_file.exists():
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                    print(f"  ✅ [{lang_code}] Valid")
                except:
                    print(f"  ❌ [{lang_code}] Invalid JSON")
        else:
            # Write the file
            if lang_file.exists():
                print(f"  🔄 [{lang_code}] Updating existing file")
                updated_count += 1
            else:
                print(f"  ✨ [{lang_code}] Creating new file")
                generated_count += 1
            
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(nested_trans, f, indent=4, ensure_ascii=False)
    
    if not validate_only:
        print(f"\n✅ Generated: {generated_count} new, updated: {updated_count} existing language files")

def main():
    parser = argparse.ArgumentParser(description="Fill missing translation keys")
    parser.add_argument('--mode', choices=['legacy', 'master'], default='legacy',
                        help='Mode: legacy (use en.json) or master (use translation_master.json)')
    parser.add_argument('--validate', action='store_true',
                        help='Validation only mode (no file modifications)')
    
    args = parser.parse_args()
    
    if args.mode == 'legacy':
        fill_missing_keys_legacy()
    elif args.mode == 'master':
        fill_missing_keys_master(validate_only=args.validate)

if __name__ == "__main__":
    main()
