import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from core.services.i18n_service import I18nService

def debug_key():
    print("🔍 Debugging 'menu.tools' key resolution...\n")
    
    i18n = I18nService()
    
    # Check English
    i18n.set_language("en")
    val = i18n.tr("menu.tools", "DEFAULT_VALUE")
    print(f"['en'] menu.tools -> '{val}'")
    
    # Check raw dict
    if "en" in i18n.translations:
        data = i18n.translations["en"]
        if "menu" in data:
            print(f"['en'] raw menu.tools -> '{data['menu'].get('tools', 'MISSING')}'")
        else:
            print("['en'] raw 'menu' block MISSING")
    else:
        print("['en'] translation dict MISSING")

if __name__ == "__main__":
    debug_key()
