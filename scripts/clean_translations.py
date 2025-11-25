"""
Script to remove hardcoded emojis from the 'lang' section of translation files.
"""
import json
import re
from pathlib import Path

def strip_emojis(text):
    # Remove flag emojis (regional indicator symbols)
    text = re.sub(r'[\U0001F1E6-\U0001F1FF]{2}', '', text)
    # Remove other common emojis
    text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)
    # Remove specific ones found in the file
    text = text.replace("🕰️", "").replace("🔴", "").replace("💀", "").replace("🎭", "").replace("🍎", "").replace("⬆️", "")
    return text.strip()

def process_file(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'lang' in data:
        count = 0
        for key, value in data['lang'].items():
            if isinstance(value, str):
                new_value = strip_emojis(value)
                if new_value != value:
                    data['lang'][key] = new_value
                    count += 1
        print(f"  Updated {count} entries.")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

base_dir = Path("i18n/translations")
process_file(base_dir / "de.json")
process_file(base_dir / "en.json")
