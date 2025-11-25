import json
import os
from pathlib import Path

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def audit_translations():
    base_path = Path("i18n/translations")
    de_file = base_path / "de.json"
    
    print(f"🔍 Auditing translations against MASTER: {de_file.name}\n")
    
    with open(de_file, 'r', encoding='utf-8') as f:
        de_data = json.load(f)
    
    de_flat = flatten_dict(de_data)
    total_keys = len(de_flat)
    print(f"Master keys found: {total_keys}")
    
    files = list(base_path.glob("*.json"))
    files.sort()
    
    results = {}
    
    for file_path in files:
        if file_path.name == "de.json":
            continue
            
        lang_code = file_path.stem
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            flat = flatten_dict(data)
            
            missing = []
            identical = [] # Potential fallback errors
            
            for key, de_val in de_flat.items():
                if key not in flat:
                    missing.append(key)
                else:
                    val = flat[key]
                    # Check for identical values (suspicious for different languages)
                    # Ignore short words or numbers which might be same
                    if val == de_val and len(str(val)) > 3 and lang_code not in ["de_at", "de_ch", "de_luxembourg"]: 
                        # Exclude dialects that might legitimately be same as standard German
                        identical.append((key, val))
            
            results[lang_code] = {
                "missing": missing,
                "identical": identical,
                "total": len(flat)
            }
            
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")

    # Report
    print("\n" + "="*60)
    print("AUDIT REPORT")
    print("="*60)
    
    suspicious_langs = []
    
    for lang, res in results.items():
        missing_count = len(res['missing'])
        identical_count = len(res['identical'])
        
        status = "✅ OK"
        if missing_count > 0:
            status = f"❌ MISSING {missing_count}"
        elif identical_count > (total_keys * 0.5): # If > 50% identical
            status = f"⚠️  SUSPICIOUS ({identical_count} identical)"
            
        print(f"{lang:<15} | Keys: {res['total']}/{total_keys} | {status}")
        
        if missing_count > 0 or identical_count > (total_keys * 0.8):
            suspicious_langs.append(lang)

    print("\n" + "="*60)
    print("DETAILED ISSUES (Top 5)")
    print("="*60)
    
    # Check English specifically
    if "en" in results:
        en_res = results["en"]
        print(f"\n🇬🇧 ENGLISH Analysis:")
        if "menu.tools" in en_res['missing']:
            print("  ❌ CRITICAL: 'menu.tools' is MISSING in en.json!")
        elif "menu.tools" in [k for k,v in en_res['identical']]:
             print(f"  ⚠️  WARNING: 'menu.tools' is identical to German ('{de_flat['menu.tools']}')")
        else:
             print("  ✅ 'menu.tools' seems correct.")
             
        if en_res['missing']:
            print(f"  Missing Keys: {en_res['missing'][:5]} ...")

if __name__ == "__main__":
    audit_translations()
