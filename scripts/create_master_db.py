#!/usr/bin/env python3
"""
Script to create translation_master.json from existing en.json and de.json
Converts flat translation files into hierarchical master database format
"""
import json
from pathlib import Path
from datetime import datetime

def load_json(file_path):
    """Load and return JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested dictionary with dot notation"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def categorize_key(key):
    """Categorize translation key based on prefix"""
    if key.startswith('menu'):
        return 'ui.menu'
    elif key.startswith('tooltips'):
        return 'ui.tooltip'
    elif key.startswith('dialogs'):
        return 'ui.dialog'
    elif key.startswith('widgets'):
        return 'ui.widget'
    elif key.startswith('tabs'):
        return 'ui.tab'
    elif key.startswith('weather'):
        return 'data.weather'
    elif key.startswith('time'):
        return 'data.time'
    elif key.startswith('network'):
        return 'data.network'
    elif key.startswith('units'):
        return 'data.units'
    elif key.startswith('status'):
        return 'data.status'
    elif key.startswith('media'):
        return 'feature.media'
    elif key.startswith('file_manager'):
        return 'feature.file_manager'
    elif key.startswith('disk_io'):
        return 'feature.disk_io'
    elif key.startswith('gauges'):
        return 'ui.gauge'
    elif key.startswith('lang'):
        return 'meta.language_names'
    elif key.startswith('menu_languages'):
        return 'meta.language_groups'
    else:
        return 'other'

def is_critical(key):
    """Determine if a translation key is critical for UI"""
    critical_prefixes = ['menu', 'dialogs', 'tabs']
    return any(key.startswith(prefix) for prefix in critical_prefixes)

def create_master_database():
    """Create master translation database from en.json and de.json"""
    
    # Paths
    translations_dir = Path("i18n/translations")
    en_file = translations_dir / "en.json"
    de_file = translations_dir / "de.json"
    master_file = Path("i18n/translation_master.json")
    
    print("🔧 Creating Master Translation Database...")
    print(f"   Reading: {en_file}")
    print(f"   Reading: {de_file}")
    
    # Load existing translations
    en_data = load_json(en_file)
    de_data = load_json(de_file)
    
    # Flatten both
    en_flat = flatten_dict(en_data)
    de_flat = flatten_dict(de_data)
    
    # Get all unique keys
    all_keys = set(list(en_flat.keys()) + list(de_flat.keys()))
    
    print(f"   Found {len(all_keys)} unique translation keys")
    
    # Build master database
    translations = {}
    for key in sorted(all_keys):
        en_value = en_flat.get(key, "")
        de_value = de_flat.get(key, en_value)  # Fallback to English if missing
        
        translations[key] = {
            "context": f"Translation for '{key}'",
            "category": categorize_key(key),
            "priority": "critical" if is_critical(key) else "normal",
            "values": {
                "en": en_value,
                "de": de_value
            }
        }
    
    # Create master database structure
    master_db = {
        "metadata": {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "total_keys": len(translations),
            "supported_languages": ["en", "de"],
            "description": "Central translation database - Source of truth for MacGyver Multi-Tool"
        },
        "translations": translations
    }
    
    # Ensure directory exists
    master_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write master database
    print(f"   Writing: {master_file}")
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Master Translation Database created successfully!")
    print(f"   Total translations: {len(translations)}")
    print(f"   Languages: en, de")
    print(f"   Location: {master_file.absolute()}")
    
    # Summary by category
    categories = {}
    for trans in translations.values():
        cat = trans['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Translations by category:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}")

if __name__ == "__main__":
    create_master_database()
