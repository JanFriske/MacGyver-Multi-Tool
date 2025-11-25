"""Erstelle Sprachdateien für Phase 4.5"""
import json
from pathlib import Path

# Template laden
template_file = Path(__file__).parent.parent / "i18n" / "translations" / "en.json"
with open(template_file, "r", encoding="utf-8") as f:
    template = json.load(f)

translations_dir = Path(__file__).parent.parent / "i18n" / "translations"

new_langs = {
    "la": "Latin",
    "eo": "Esperanto",
    "ia": "Interlingua"
}

print("Erstelle Sprachdateien für Phase 4.5:")
print("=" * 40)

for code, name in new_langs.items():
    output_file = translations_dir / f"{code}.json"
    if not output_file.exists():
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(template, f, ensure_ascii=False, indent=4)
        print(f"✅ {code:5s} - {name}")
    else:
        print(f"⚠️ {code:5s} - {name} (existiert bereits)")

print("=" * 40)
print("Fertig.")
