import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService

def main():
    print("Verifying Language Groups...")
    service = I18nService()
    groups = service.get_language_groups()
    
    # Check for new Top Groups
    expected_top_groups = ["🇩🇪 Deutsch", "🇬🇧 English", "🇫🇷 Français", "🇪🇸 Español", "🇵🇹 Português"]
    for group in expected_top_groups:
        if group in groups:
            print(f"✅ Found Top Group: {group}")
            # Check subgroups
            subgroups = groups[group]
            for sub, langs in subgroups.items():
                print(f"  - {sub}: {list(langs.keys())}")
        else:
            print(f"❌ Missing Top Group: {group}")

    # Check for Pirate Dialects
    print("\nChecking Pirate Dialects:")
    
    pirate_checks = {
        "🇩🇪 Deutsch": ["de_pirate"],
        "🇬🇧 English": ["en_pirate"],
        "🇫🇷 Français": ["fr_pirate", "fr_CA_pirate"],
        "🇪🇸 Español": ["es_pirate"],
        "🇵🇹 Português": ["pt_pirate"],
        "🌍 Europa": ["it_pirate", "nl_pirate", "sco_pirate", "ru_pirate", "pl_pirate"],
        "🌏 Asien": ["ja_pirate", "zh_pirate"],
        "🌍 Naher Osten & Afrika": ["tr_pirate"],
        "🏛️ Klassisch & Konstruiert": ["tlh_pirate"]
    }

    all_found = True
    for group_name, expected_langs in pirate_checks.items():
        group = groups.get(group_name, {})
        found_in_group = []
        for sub, langs in group.items():
            found_in_group.extend(langs.keys())
        
        for lang in expected_langs:
            if lang in found_in_group:
                print(f"✅ Found '{lang}' in '{group_name}'")
            else:
                print(f"❌ '{lang}' NOT found in '{group_name}'")
                all_found = False
    
    if all_found:
        print("\n✅ All 15 Pirate dialects verified!")
    else:
        print("\n❌ Some Pirate dialects are missing!")

if __name__ == "__main__":
    main()
