"""
Test Translations
Verifies that the new menu_languages keys are correctly loaded for en, de, and de_middlehigh.
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from core.services.i18n_service import I18nService

def test_translations():
    print("🧪 Testing Translations...\n")
    
    i18n = I18nService()
    
    test_cases = [
        ("en", "menu_languages.main", "🌍 Main Languages"),
        ("de", "menu_languages.main", "🌍 Hauptsprachen"),
        ("de_middlehigh", "menu_languages.main", "🌍 Houpt Zungen"),
        ("en", "menu_languages.german", "🇩🇪 German"),
        ("de", "menu_languages.german", "🇩🇪 Deutsch"),
        ("de_middlehigh", "menu_languages.german", "🇩🇪 Diutsch"),
    ]
    
    passed = 0
    failed = 0
    
    for lang, key, expected in test_cases:
        i18n.set_language(lang)
        result = i18n.tr(key)
        
        if result == expected:
            print(f"✅ [{lang}] {key} -> '{result}'")
            passed += 1
        else:
            print(f"❌ [{lang}] {key} -> '{result}' (Expected: '{expected}')")
            failed += 1
            
    print("\n" + "="*30)
    if failed == 0:
        print(f"🎉 All {passed} tests passed!")
    else:
        print(f"⚠️  {failed} tests failed.")

if __name__ == "__main__":
    test_translations()
