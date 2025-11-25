"""Finde die letzte fehlende MS Store Sprache"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.i18n_service import I18nService

# Load MS Store languages
ms_file = Path(__file__).parent.parent / "docs" / "microsoft_store_languages.json"
with open(ms_file, "r", encoding="utf-8") as f:
    ms_data = json.load(f)

# Get MacGyver languages
i18n = I18nService()
mg_langs = set(code.lower().replace('_', '').replace('-', '') for code in i18n.get_all_language_codes())

print("=" * 80)
print("DIE LETZTE FEHLENDE SPRACHE")
print("=" * 80)
print()

for lang in ms_data['languages']:
    code_normalized = lang['code'].lower().replace('_', '').replace('-', '')
    
    if code_normalized not in mg_langs:
        print(f"Code:   {lang['code']}")
        print(f"Name:   {lang['name']}")
        print(f"Native: {lang['native_name']}")
        print(f"BCP-47: {lang['bcp47']}")
        print()
