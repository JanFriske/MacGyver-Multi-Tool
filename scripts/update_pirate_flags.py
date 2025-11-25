
import json
from pathlib import Path

flags_path = Path("i18n/flags.json")

with open(flags_path, "r", encoding="utf-8") as f:
    flags = json.load(f)

# Update all pirate dialects to use 'pirate' flag
pirate_langs = [
    "de_pirate", "en_pirate", "es_pirate", "fr_pirate", "fr_CA_pirate",
    "ja_pirate", "nl_pirate", "pl_pirate", "pt_pirate", "ru_pirate",
    "sco_pirate", "tlh_pirate", "tr_pirate", "zh_pirate"
]

count = 0
for lang in pirate_langs:
    if lang in flags:
        flags[lang] = "pirate"
        count += 1

with open(flags_path, "w", encoding="utf-8") as f:
    json.dump(flags, f, indent=4, sort_keys=True)

print(f"Updated {count} pirate flags.")
