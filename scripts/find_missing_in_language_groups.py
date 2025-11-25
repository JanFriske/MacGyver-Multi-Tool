#!/usr/bin/env python3
"""
Analyze which .json files exist but are not registered in LANGUAGE_GROUPS
"""
import json
import sys
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent.parent))

from core.services.i18n_service import I18nService

# Get all .json files
translations_dir = Path("i18n/translations")
all_json_files = sorted([f.stem for f in translations_dir.glob("*.json")])

print(f"📁 Found {len(all_json_files)} .json files in {translations_dir}")

# Get all registered languages in LANGUAGE_GROUPS
service = I18nService()
registered_codes = service.get_all_language_codes()

print(f"📝 Found {len(registered_codes)} languages registered in LANGUAGE_GROUPS")

# Find missing
missing = sorted(set(all_json_files) - set(registered_codes))

print("\n" + "=" * 60)
print(f"🔍 Missing from LANGUAGE_GROUPS: {len(missing)}")
print("=" * 60)

if missing:
    print("\nThese .json files exist but are NOT in LANGUAGE_GROUPS:\n")
    for lang_code in missing:
        print(f"  ❌ {lang_code}.json")
    
    # Categorize by pattern
    print("\n📊 Categorization:")
    
    de_dialects = [l for l in missing if l.startswith('de_')]
    french = [l for l in missing if l in ['oc', 'br', 'co'] or l.startswith('fr_') and l not in registered_codes]
    italian = [l for l in missing if l in ['vec', 'nap', 'scn', 'lmo', 'it_tuscany']]
    spanish = [l for l in missing if l.startswith('es_') and l not in registered_codes]
    polish = [l for l in missing if l in ['szl', 'csb']]
    dutch = [l for l in missing if l in ['li', 'fy']]
    others = [l for l in missing if l not in de_dialects + french + italian + spanish + polish + dutch]
    
    if de_dialects:
        print(f"\n  🇩🇪 German: {len(de_dialects)}")
        for l in de_dialects:
            print(f"     - {l}")
    
    if french:
        print(f"\n  🇫🇷 French: {len(french)}")
        for l in french:
            print(f"     - {l}")
    
    if italian:
        print(f"\n  🇮🇹 Italian: {len(italian)}")
        for l in italian:
            print(f"     - {l}")
    
    if spanish:
        print(f"\n  🇪🇸 Spanish: {len(spanish)}")
        for l in spanish:
            print(f"     - {l}")
    
    if polish:
        print(f"\n  🇵🇱 Polish: {len(polish)}")
        for l in polish:
            print(f"     - {l}")
    
    if dutch:
        print(f"\n  🇳🇱 Dutch: {len(dutch)}")
        for l in dutch:
            print(f"     - {l}")
    
    if others:
        print(f"\n  🌍 Others: {len(others)}")
        for l in others:
            print(f"     - {l}")

else:
    print("\n✅ All .json files are registered in LANGUAGE_GROUPS!")

print("\n" + "=" * 60)
