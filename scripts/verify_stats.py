import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService

def main():
    print("Verifying Statistics Accuracy...")
    service = I18nService()
    
    # Calculate all stats once
    all_stats = service.get_translation_stats()
    
    # 1. Check English (Base)
    if "en" in all_stats:
        stats_en = all_stats["en"]
        print(f"EN Stats: {stats_en['percent']}% ({stats_en['translated_keys']}/{stats_en['total_keys']})")
        
        if stats_en['percent'] == 100:
            print("✅ EN is 100%")
        else:
            print(f"⚠️ EN is not 100%? Missing: {stats_en['missing_keys']}")
    else:
        print("❌ EN stats not found!")

    # 2. Check German
    if "de" in all_stats:
        stats_de = all_stats["de"]
        print(f"DE Stats: {stats_de['percent']}%")
    else:
        print("❌ DE stats not found!")
    
    # 3. Check a Pirate Language
    if "fr_pirate" in all_stats:
        stats_fr_pirate = all_stats["fr_pirate"]
        print(f"FR Pirate Stats: {stats_fr_pirate['percent']}%")
    else:
        print("❌ FR Pirate stats not found!")
    
    # 4. Check Consistency
    if "en" in all_stats and "de" in all_stats:
        total_keys = all_stats["en"]['total_keys']
        if all_stats["de"]['total_keys'] == total_keys:
            print(f"✅ Total keys consistent: {total_keys}")
        else:
            print(f"❌ Total keys inconsistent: EN={total_keys}, DE={all_stats['de']['total_keys']}")

if __name__ == "__main__":
    main()
