"""
Compare flags.json keys with LANGUAGE_GROUPS to find missing languages.
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from core.services.i18n_service import I18nService

service = I18nService()
# Get all language codes currently in the menu
menu_codes = set(service.get_all_language_codes())

# Get all language codes we have flags for (implies we expect to support them)
with open("i18n/flags.json", "r", encoding="utf-8") as f:
    flags_map = json.load(f)
    flag_codes = set(flags_map.keys())

# Find codes in flags.json that are NOT in the menu
missing = flag_codes - menu_codes

print(f"Menu has {len(menu_codes)} languages.")
print(f"Flags.json has {len(flag_codes)} languages.")
print(f"Missing from menu: {len(missing)}")

if missing:
    print("Missing codes:", sorted(list(missing)))
