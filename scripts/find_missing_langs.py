"""Finde fehlende MS Store Sprachen"""
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
mg_langs = set(i18n.get_all_language_codes())

print("Fehlende Microsoft Store Sprachen:")
print("=" * 60)

missing_count = 0
for lang in ms_data['languages']:
    code = lang['code']
    # Check various possible mappings
    possible_codes = [
        code,
        code.replace('-', '_'),
        code.replace('_', '-'),
        code.split('-')[0],
        code.split('_')[0]
    ]
    
    found = any(pc in mg_langs for pc in possible_codes)
    
    if not found:
        missing_count += 1
        print(f"{missing_count:2d}. {code:15s} - {lang['name']:30s} ({lang['native_name']})")

print("=" * 60)
print(f"Gesamt fehlend: {missing_count}")
