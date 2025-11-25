import json
import os
from pathlib import Path

# Base directory for translations
TRANS_DIR = Path(r"c:\Dev\Repos\JanFriske\MacGyver Multi-Tool\i18n\translations")

# Template: Load en_pirate.json
template_path = TRANS_DIR / "en_pirate.json"
if not template_path.exists():
    print(f"Error: Template {template_path} not found!")
    exit(1)

with open(template_path, "r", encoding="utf-8") as f:
    template_data = json.load(f)

# List of new pirate languages to create
new_pirate_langs = {
    "fr_pirate": "🏴‍☠️ Français Pirate",
    "es_pirate": "🏴‍☠️ Español Pirate",
    "pt_pirate": "🏴‍☠️ Português Pirate",
    "sco_pirate": "🏴‍☠️ Scots Pirate",
    "tlh_pirate": "🏴‍☠️ Klingon Pirate",
    "fr_CA_pirate": "🏴‍☠️ Québécois Pirate",
    "it_pirate": "🏴‍☠️ Italiano Pirate",
    "nl_pirate": "🏴‍☠️ Nederlands Pirate",
    "ru_pirate": "🏴‍☠️ Russian Pirate",
    "pl_pirate": "🏴‍☠️ Polish Pirate",
    "tr_pirate": "🏴‍☠️ Turkish Pirate",
    "ja_pirate": "🏴‍☠️ Japanese Pirate",
    "zh_pirate": "🏴‍☠️ Chinese Pirate"
}

for code, name in new_pirate_langs.items():
    file_path = TRANS_DIR / f"{code}.json"
    
    # Create a copy of the template
    new_data = template_data.copy()
    
    # Update the self-reference in the 'lang' section
    if "lang" not in new_data:
        new_data["lang"] = {}
    
    new_data["lang"][code] = name
    
    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    
    print(f"Created {code}.json ({name})")

print("Done!")
