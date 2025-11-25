"""
Debug Script for I18nService
Tests language loading, switching, and translation retrieval
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from core.services.i18n_service import I18nService

def test_i18n():
    print("="*60)
    print("I18nService DIAGNOSTIC TEST")
    print("="*60)
    
    # 1. Initialize Service
    print("\n[1] Initializing Service...")
    try:
        service = I18nService()
        print("✅ Service initialized")
    except Exception as e:
        print(f"❌ Service init failed: {e}")
        return

    # 2. Check Loaded Languages
    print("\n[2] Checking Loaded Languages...")
    codes = service.get_all_language_codes()
    print(f"Total codes found: {len(codes)}")
    
    critical_langs = ["de", "en", "de_middlehigh", "ko"]
    for lang in critical_langs:
        if lang in codes:
            print(f"✅ {lang} found in codes")
        else:
            print(f"❌ {lang} NOT found in codes!")
            
    # 3. Check Translations Content
    print("\n[3] Checking Translation Content...")
    for lang in critical_langs:
        data = service.translations.get(lang)
        if data:
            key_count = len(str(data)) # Rough size check
            print(f"✅ {lang} loaded (size: {key_count} chars)")
        else:
            print(f"❌ {lang} NOT loaded (empty or None)")

    # 4. Test Switching and Translation
    print("\n[4] Testing Switching & Translation (Key: 'menu.file')...")
    
    test_cases = [
        ("de", "Datei"),
        ("en", "File"),
        ("de_middlehigh", "Datei"), # Should be same as DE for now
        ("ko", "파일") # Should be Korean
    ]
    
    for lang, expected in test_cases:
        print(f"\n--- Switching to {lang} ---")
        service.set_language(lang)
        
        if service.current_language != lang:
            print(f"❌ Failed to set language to {lang}. Current: {service.current_language}")
            continue
            
        result = service.tr("menu.file")
        print(f"Result: '{result}'")
        
        if result == expected:
            print(f"✅ Correct: {result}")
        elif lang == "en" and result == "Datei":
             print(f"❌ ERROR: English returned German text! (Fallback active?)")
        else:
            print(f"⚠️  Mismatch: Expected '{expected}', got '{result}'")

if __name__ == "__main__":
    test_i18n()
