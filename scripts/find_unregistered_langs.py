"""Finde Sprachen die in Dateien existieren aber nicht in LANGUAGE_GROUPS"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.i18n_service import I18nService

# Get all language codes from LANGUAGE_GROUPS
i18n = I18nService()
registered_codes = set(i18n._get_all_language_codes())

# Get all translation files
translations_dir = Path(__file__).parent.parent / "i18n" / "translations"
file_codes = set()
for file in translations_dir.glob("*.json"):
    if not file.stem.endswith('.corrupted'):
        file_codes.add(file.stem)

# Find unregistered
unregistered = file_codes - registered_codes

print("=" * 80)
print("NICHT REGISTRIERTE SPRACHEN")
print("=" * 80)
print(f"\nDateien gesamt: {len(file_codes)}")
print(f"Registriert:    {len(registered_codes)}")
print(f"Nicht registriert: {len(unregistered)}")
print()

if unregistered:
    print("Folgende Sprachdateien existieren, sind aber nicht in LANGUAGE_GROUPS:")
    for code in sorted(unregistered):
        print(f"  - {code}")
else:
    print("✅ Alle Sprachdateien sind registriert!")
