"""
Deep Debug for I18nService.tr()
"""
import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from core.services.i18n_service import I18nService

def debug_tr():
    print("="*60)
    print("DEEP DEBUG: I18nService.tr()")
    print("="*60)
    
    service = I18nService()
    
    # Force load English
    print("\n[1] Checking English Data...")
    en_data = service.translations.get("en")
    if not en_data:
        print("❌ English data NOT loaded!")
        return
    
    print(f"✅ English data loaded. Keys: {list(en_data.keys())}")
    
    if "menu" in en_data:
        print(f"✅ 'menu' found in en_data. Type: {type(en_data['menu'])}")
        if isinstance(en_data["menu"], dict):
            print(f"   Keys in 'menu': {list(en_data['menu'].keys())}")
            if "file" in en_data["menu"]:
                print(f"✅ 'file' found in 'menu'. Value: '{en_data['menu']['file']}'")
            else:
                print("❌ 'file' NOT found in 'menu'")
        else:
            print("❌ 'menu' is NOT a dict")
    else:
        print("❌ 'menu' NOT found in en_data")

    # Test tr() manually
    print("\n[2] Testing tr('menu.file') manually...")
    service.current_language = "en"
    
    key = "menu.file"
    keys = key.split(".")
    value = en_data
    
    print(f"Start Value: (dict with {len(value)} keys)")
    
    for k in keys:
        print(f"Looking for '{k}'...")
        if isinstance(value, dict):
            value = value.get(k)
            print(f" -> Found: {value} (Type: {type(value)})")
        else:
            print(f" -> Value is not dict, cannot look up '{k}'")
            break
            
    if value and isinstance(value, str):
        print(f"✅ Manual lookup success: '{value}'")
    else:
        print(f"❌ Manual lookup failed. Result: {value}")

    # Test actual tr() method
    print("\n[3] Testing service.tr('menu.file')...")
    service.set_language("en")
    result = service.tr("menu.file")
    print(f"Result: '{result}'")
    
    if result == "File":
        print("✅ SUCCESS")
    else:
        print(f"❌ FAILURE: Expected 'File', got '{result}'")

if __name__ == "__main__":
    debug_tr()
