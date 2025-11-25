"""
Test German Language Names
Verifies that the `lang.*` keys are correctly translated when the language is set to German.
"""
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from core.services.i18n_service import I18nService

def verify_german_lang_names():
    print("🧪 Verifying German Language Name Translations...\n")
    
    i18n = I18nService()
    i18n.set_language("de")
    
    # A representative sample of languages to test
    test_cases = {
        "en": "Englisch",
        "de": "Hochdeutsch",
        "ja": "Japanisch",
        "ru": "Russisch",
        "zh-Hans": "Chinesisch (Vereinfacht)",
        "es_MX": "Spanisch (Mexiko)",
        "fr_CA": "Französisch (Kanada)",
        "de_bavaria": "Bairisch",
        "am": "Amharisch",
        "ti": "Tigrinisch",
        "pl": "Polnisch",
        "el": "Griechisch",
        "ko": "Koreanisch",
        "hi": "Hindi",
        "ar": "Arabisch",
        "he": "Hebräisch",
    }
    
    passed = 0
    failed = 0
    
    for lang_code, expected_german_name in test_cases.items():
        key = f"lang.{lang_code}"
        result = i18n.tr(key)
        
        if result == expected_german_name:
            print(f"✅ [de] {key} -> '{result}'")
            passed += 1
        else:
            # Fallback check for keys that might not exist, tr() returns the key
            if result == key:
                print(f"❌ [de] {key} -> FAILED (Key not found, returned key)")
            else:
                 print(f"❌ [de] {key} -> FAILED (Got: '{result}', Expected: '{expected_german_name}')")
            failed += 1
            
    print("\n" + "="*40)
    if failed == 0:
        print(f"🎉 All {passed} German language name translation tests passed!")
        return True
    else:
        print(f"⚠️  {failed} of {len(test_cases)} tests failed.")
        return False

if __name__ == "__main__":
    if not verify_german_lang_names():
        sys.exit(1)
