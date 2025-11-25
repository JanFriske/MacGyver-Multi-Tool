"""
Analyze missing UN official languages based on countries_un_official.md
Compares with existing i18n language files to identify gaps.
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService

# UN Official languages from countries_un_official.md
UN_LANGUAGES = {
    # Afrika
    "ar": "Arabisch",  # Already have
    "am": "Amharisch",  # Already have
    "ti": "Tigrinya",  # Already have
    "so": "Somali",  # MISSING
    "sw": "Swahili",  # Already have (Kiswahili)
    "rw": "Kinyarwanda",  # Already have
    "sg": "Sango",  # MISSING
    "mg": "Malagasy",  # MISSING
    "crs": "Seychellenkreol",  # MISSING
    
    # Asien
    "ps": "Pashtu",  # MISSING
    "prs": "Dari",  # Already have (fa_AF)
    "dz": "Dzongkha",  # MISSING
    "my": "Birmanisch",  # Already have
    "lo": "Laotisch",  # Already have
    "km": "Khmer",  # Already have
    "vi": "Vietnamesisch",  # Already have
    "th": "Thailändisch",  # Already have
    "ms": "Malaiisch",  # Already have
    "id": "Indonesisch",  # Already have
    "tl": "Filipino/Tagalog",  # Already have (fil)
    
    # Ozeanien
    "sm": "Samoanisch",  # MISSING
    "to": "Tongaisch",  # MISSING
    "fj": "Fidschi",  # MISSING
    "hif": "Fidschi-Hindi",  # MISSING
    "bi": "Bislama",  # MISSING
    "tpi": "Tok Pisin",  # MISSING
    "ho": "Hiri Motu",  # MISSING
    "gil": "Kiribatisch",  # MISSING
    "mh": "Marshallisch",  # MISSING
    "na": "Nauruisch",  # MISSING
    "pau": "Palauisch",  # MISSING
    "tvl": "Tuvaluisch",  # MISSING
    
    # Südamerika
    "gn": "Guaraní",  # MISSING
    "ay": "Aymara",  # MISSING
    "qu": "Quechua",  # Already have (quz)
    
    # Afrika/Karibik
    "ht": "Haitianisch-Kreolisch",  # MISSING
    
    # Andere
    "tet": "Tetum",  # MISSING (Timor-Leste)
}

def main():
    print("Analyzing Missing UN Official Languages...")
    print("=" * 60)
    
    service = I18nService()
    existing_codes = service.get_all_language_codes()
    
    missing = []
    found = []
    
    for code, name in UN_LANGUAGES.items():
        if code in existing_codes:
            found.append(f"✅ {code}: {name}")
        else:
            missing.append(f"❌ {code}: {name}")
    
    print(f"\n📊 Summary:")
    print(f"Total UN Languages Analyzed: {len(UN_LANGUAGES)}")
    print(f"Already Implemented: {len(found)}")
    print(f"Missing: {len(missing)}")
    
    if found:
        print(f"\n✅ Already Implemented ({len(found)}):")
        for lang in found:
            print(f"  {lang}")
    
    if missing:
        print(f"\n❌ Missing Languages ({len(missing)}):")
        for lang in missing:
            print(f"  {lang}")
        
        print(f"\n📝 Next Steps:")
        print(f"1. Create JSON files for {len(missing)} missing languages")
        print(f"2. Register in LANGUAGE_GROUPS with geographic categories")
        print(f"3. Add ☠️ icons for Pirate variants")
        print(f"4. Add flag emojis for country languages")

if __name__ == "__main__":
    main()
