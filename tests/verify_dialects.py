import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService

def test_dialects():
    print("Testing Dialect Loading...")
    i18n = I18nService()
    
    dialects = [
        "de_bavaria", 
        "de_swabian", 
        "de_saxony", 
        "de_ripuarian", 
        "de_at"
    ]
    
    # 1. Verify Dialects are Loaded
    available_langs = i18n.get_all_language_codes()
    print(f"Total languages loaded: {len(available_langs)}")
    
    all_loaded = True
    for dialect in dialects:
        if dialect in available_langs:
            print(f"   ✅ Loaded: {dialect} ({i18n.get_language_name(dialect)})")
        else:
            print(f"   ❌ Failed to load: {dialect}")
            all_loaded = False
            
    if not all_loaded:
        print("❌ Not all dialects loaded!")
        return

    # 2. Verify Translation Content
    print("\nVerifying Translation Content (Key: menu.file)...")
    
    test_key = "menu.file"
    
    for dialect in dialects:
        i18n.set_language(dialect)
        trans = i18n.tr(test_key)
        print(f"   {dialect}: {trans}")
        
        # Basic check - should not be empty or key itself
        if trans and trans != test_key:
             pass # Good
        else:
             print(f"   ⚠️ Warning: Translation for {test_key} in {dialect} seems missing or default.")

    print("\n✅ Dialect verification complete.")

if __name__ == "__main__":
    test_dialects()
