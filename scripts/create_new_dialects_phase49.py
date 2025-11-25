#!/usr/bin/env python3
"""
Create new dialect JSON files for Phase 4.9
Uses en.json as template
"""
import json
from pathlib import Path

# Base directory
translations_dir = Path("i18n/translations")
template_file = translations_dir / "en.json"

# Load template
with open(template_file, 'r', encoding='utf-8') as f:
    template = json.load(f)

# Define new dialects to create
new_dialects = {
    # German Swiss (3)
    "de_CH_zurich": "Zürichdeutsch",
    "de_CH_bern": "Berndeutsch",
    "de_CH_basel": "Baseldeutsch",
    
    # Austrian (1)
    "de_AT_carinthia": "Kärntnerisch",
    
    # German border regions (2)
    "de_FR_alsace": "Elsässisch (Frankreich)",
    
    # Silesian sub-dialects (2)
    "de_silesian_upper": "Oberschlesisch",
    "de_silesian_lower": "Niederschlesisch",
    
    # East Prussian (1)
    "de_eastprussia_lithuanian": "Ostpreußisch-Litauisch",
    
    # French dialects (3)
    "oc": "Occitan (Okzitanisch)",
    "br": "Brezhoneg (Bretonisch)",
    "co": "Corsu (Korsisch)",
    
    # Spanish (1)
    "es_andalucia": "Andaluz (Andalusisch)",
    
    # Italian dialects (5)
    "it_tuscany": "Toscano (Toskanisch)",
    "vec": "Vèneto (Venetisch)",
    "nap": "Napulitano (Neapolitanisch)",
    "scn": "Sicilianu (Sizilianisch)",
    "lmo": "Lumbaart (Lombardisch)",
    
    # Polish (2)
    "szl": "Ślōnsko godka (Schlesisch)",
    "csb": "Kaszëbsczi (Kaschubisch)",
    
    # Dutch (2)
    "li": "Limburgs (Limburgisch)",
    "fy": "Frysk (Friesisch)",
}

print(f"Creating {len(new_dialects)} new dialect files...")
print("=" * 60)

created_count = 0
skipped_count = 0

for lang_code, lang_name in new_dialects.items():
    target_file = translations_dir / f"{lang_code}.json"
    
    if target_file.exists():
        print(f"⏭️  SKIP: {lang_code}.json already exists")
        skipped_count += 1
        continue
    
    # Write template to new file
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"✅ CREATE: {lang_code}.json ({lang_name})")
    created_count += 1

print("=" * 60)
print(f"\n📊 Summary:")
print(f"   ✅ Created: {created_count}")
print(f"   ⏭️  Skipped: {skipped_count}")
print(f"   📁 Total: {len(new_dialects)}")
print(f"\n✅ All dialect files ready!")
