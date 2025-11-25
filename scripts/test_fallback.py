import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService

def main():
    print("Testing I18n Fallback Logic...")
    service = I18nService()
    
    # 1. Test Key Existence (No Fallback needed)
    service.set_language("de")
    val = service.tr("menu.file")
    print(f"DE 'menu.file': {val} (Expected: Datei) -> {'✅' if val == 'Datei' else '❌'}")
    
    service.set_language("en")
    val = service.tr("menu.file")
    print(f"EN 'menu.file': {val} (Expected: File) -> {'✅' if val == 'File' else '❌'}")
    
    # 2. Test Fallback to DE (if current is not DE/EN and key missing)
    # We need a language that is NOT de or en. Let's use 'fr' (if exists) or a fake one.
    # We'll use 'fr' and assume it doesn't have a specific key that DE has.
    # Or better, let's use a non-existent key in 'fr' but existent in 'de'.
    
    # Let's use a custom key that we know only exists in DE (or we inject it)
    # Since we can't easily inject without writing files, let's use a key that is likely missing in a new language.
    # 'fr' might be empty or partial.
    
    service.set_language("fr")
    # 'menu.file' should be 'Fichier' if fr.json exists and is complete. 
    # If fr.json is a placeholder (which it might be for now), it might be empty.
    # If empty, it should fallback to DE 'Datei'.
    
    val = service.tr("menu.file")
    print(f"FR 'menu.file': {val}")
    
    # 3. Test Fallback to EN (if DE is also missing)
    # We need a key that is missing in FR and DE but present in EN.
    # This is hard to guarantee without controlling the files.
    
    # 4. Test Missing Key (Fallback to Key Name)
    val = service.tr("non.existent.key")
    print(f"Missing Key: {val} (Expected: non.existent.key) -> {'✅' if val == 'non.existent.key' else '❌'}")
    
    # 5. Test Pirate Language (Special Char)
    service.set_language("en_pirate")
    val = service.tr("menu.file")
    print(f"Pirate 'menu.file': {val} (Expected: Treasure Map) -> {'✅' if val == 'Treasure Map' else '❌'}")

if __name__ == "__main__":
    main()
