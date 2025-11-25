"""
Audit all languages for missing flags.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from core.services.i18n_service import I18nService
# We need to replicate view.py's resolution logic or import it if possible.
# Importing view.py might start the app, so we'll replicate the logic.
import json

def resolve_flag_path(lang_code, service):
    path = service.get_flag_path(lang_code)
    if path:
        return path.name
    return None

service = I18nService()
all_codes = service.get_all_language_codes()
print(f"Checking {len(all_codes)} languages...")

missing = []
for code in all_codes:
    flag = resolve_flag_path(code, service)
    if not flag:
        missing.append(code)

print(f"Found {len(missing)} languages without flags:")
for m in sorted(missing):
    name = service.get_language_name(m)
    print(f" - {m}: {name}")
