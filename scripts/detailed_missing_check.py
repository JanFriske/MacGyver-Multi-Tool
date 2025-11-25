"""Detaillierte Analyse fehlender MS Store Sprachen"""
import sys
import json
from pathlib import Path

# Load MS Store languages
ms_file = Path(__file__).parent.parent / "docs" / "microsoft_store_languages.json"
with open(ms_file, "r", encoding="utf-8") as f:
    ms_data = json.load(f)

# Get existing translation files
translations_dir = Path(__file__).parent.parent / "i18n" / "translations"
existing_files = set()
for file in translations_dir.glob("*.json"):
    if not file.stem.endswith('.corrupted'):
        existing_files.add(file.stem)

print("=" * 80)
print("FEHLENDE MICROSOFT STORE SPRACHEN - DETAILLIERTE ANALYSE")
print("=" * 80)
print()

missing = []
for lang in ms_data['languages']:
    ms_code = lang['code']
    
    # Mögliche MacGyver-Mappings
    possible_codes = [
        ms_code,
        ms_code.replace('-', '_'),
        ms_code.replace('Hans', ''),
        ms_code.replace('Hant', ''),
        ms_code.replace('-', '').replace('_', ''),
    ]
    
    # Prüfe ob irgendeine Variante existiert
    found = any(pc in existing_files or pc.replace('-', '_') in existing_files for pc in possible_codes)
    
    if not found:
        missing.append(lang)

print(f"Fehlende Sprachen: {len(missing)}")
print()

for i, lang in enumerate(missing, 1):
    print(f"{i:2d}. Code: {lang['code']:20s}")
    print(f"    Name: {lang['name']}")
    print(f"    Native: {lang['native_name']}")
    print(f"    BCP-47: {lang['bcp47']}")
    print()

print("=" * 80)
print(f"GESAMT: {len(missing)} fehlende Sprachen")
print("=" * 80)
