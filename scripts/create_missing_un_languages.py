"""
Create missing UN official language JSON files
Based on countries_un_official.md analysis
"""
import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Missing UN languages to create
MISSING_LANGUAGES = {
    "so": "Somali",
    "sg": "Sango",
    "mg": "Malagasy",
    "crs": "Seychellenkreol",
    "ps": "Pashtu",
    "dz": "Dzongkha",
    "sm": "Samoanisch",
    "to": "Tongaisch",
    "fj": "Fidschi",
    "hif": "Fidschi-Hindi",
    "bi": "Bislama",
    "tpi": "Tok Pisin",
    "ho": "Hiri Motu",
    "gil": "Kiribatisch",
    "mh": "Marshallisch",
    "na": "Nauruisch",
    "pau": "Palauisch",
    "tvl": "Tuvaluisch",
    "gn": "Guaraní",
    "ay": "Aymara",
    "ht": "Haitianisch-Kreolisch",
    "tet": "Tetum",
}

def main():
    print("Creating Missing UN Language Files...")
    print("=" * 60)
    
    # Load en.json as template
    template_path = Path("i18n/translations/en.json")
    if not template_path.exists():
        print(f"❌ Template file not found: {template_path}")
        return
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    
    created_count = 0
    skipped_count = 0
    
    for code, name in MISSING_LANGUAGES.items():
        output_path = Path(f"i18n/translations/{code}.json")
        
        if output_path.exists():
            print(f"⏭️  Skipped {code}.json (already exists)")
            skipped_count += 1
            continue
        
        # Create language file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {code}.json - {name}")
        created_count += 1
    
    print(f"\n📊 Summary:")
    print(f"Created: {created_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total: {len(MISSING_LANGUAGES)}")

if __name__ == "__main__":
    main()
