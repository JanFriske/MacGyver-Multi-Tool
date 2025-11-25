"""Erstelle die letzten 10 fehlenden MS Store Sprachen"""
import json
from pathlib import Path

# Template laden
template_file = Path(__file__).parent.parent / "i18n" / "translations" / "en.json"
with open(template_file, "r", encoding="utf-8") as f:
    template = json.load(f)

# MS Store Sprachen laden
ms_file = Path(__file__).parent.parent / "docs" / "microsoft_store_languages.json"
with open(ms_file, "r", encoding="utf-8") as f:
    ms_data = json.load(f)

# Existierende Dateien
translations_dir = Path(__file__).parent.parent / "i18n" / "translations"
existing_files = set()
for file in translations_dir.glob("*.json"):
    if not file.stem.endswith('.corrupted'):
        existing_files.add(file.stem)

# Finde fehlende und erstelle sie
missing_created = []

for lang in ms_data['languages']:
    ms_code = lang['code']
    
    # MacGyver Code Mapping
    macgyver_code = ms_code.replace('-', '_')
    
    # Spezielle Mappings
    if ms_code == 'zh-Hans':
        macgyver_code = 'zh'  # Bereits vorhanden als zh
    elif ms_code == 'zh-Hant':
        macgyver_code = 'zh_Hant'  # Traditionell separat
    
    # Prüfe ob existiert
    if macgyver_code not in existing_files:
        # Erstelle Datei
        output_file = translations_dir / f"{macgyver_code}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(template, f, ensure_ascii=False, indent=4)
        missing_created.append((macgyver_code, lang['name'], lang['native_name']))
        print(f"✅ {macgyver_code:20s} - {lang['name']:30s} ({lang['native_name']})")

print()
print(f"Erstellt: {len(missing_created)} neue Sprachdateien")

if len(missing_created) == 0:
    print("✅ Alle MS Store Sprachen sind jetzt vorhanden!")
