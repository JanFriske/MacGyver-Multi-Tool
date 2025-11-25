"""Quick coverage check"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.i18n_service import I18nService
import json

# Load MS Store languages
ms_file = Path(__file__).parent.parent / "docs" / "microsoft_store_languages.json"
with open(ms_file, "r", encoding="utf-8") as f:
    ms_data = json.load(f)

# Get MacGyver languages
i18n = I18nService()
mg_langs = i18n.get_all_language_codes()

print(f"Microsoft Store: {len(ms_data['languages'])} Sprachen")
print(f"MacGyver:        {len(mg_langs)} Sprachen")

# Normalize and compare
ms_codes = {lang['code'].replace('-', '').replace('_', '').lower() for lang in ms_data['languages']}
mg_codes = {code.replace('-', '').replace('_', '').lower() for code in mg_langs}

common = ms_codes & mg_codes
coverage = (len(common) / len(ms_data['languages'])) * 100

print(f"Gemeinsam:       {len(common)} Sprachen")
print(f"Coverage:        {coverage:.1f}%")

if coverage >= 95:
    print("✅ AUSGEZEICHNET - Fast vollständige Coverage!")
elif coverage >= 80:
    print("👍 GUT - Hohe Coverage!")
else:
    print("⚠️  Noch Arbeit nötig")
