"""
Translation Script for Tier-1 Languages
Extracts critical keys and prepares translation templates
"""
import json
import os
from pathlib import Path

# Tier 1 Languages (7 total - Top Priority)
TIER_1_LANGUAGES = {
    "ko": "Korean (한국어)",
    "id": "Indonesian (Bahasa Indonesia)",
    "th": "Thai (ภาษาไทย)",
    "bn": "Bengali (বাংলা)",
    "ur": "Urdu (اردو)",
    "ps": "Pashto (پښتو)",
    "fa_AF": "Dari (دری)"
}

# Critical keys that MUST be translated for functional UI
CRITICAL_KEYS = {
    # Main Menu (8 keys)
    "menu.file": "File menu",
    "menu.edit": "Edit menu",
    "menu.view": "View menu",
    "menu.tools": "Tools menu",
    "menu.settings": "Settings menu",
    "menu.help": "Help menu",
    "menu.languages": "Languages menu",
    "menu.german_dialects": "German dialects submenu",
    
    # File Menu (4 keys)
    "menu_file.new": "New file action",
    "menu_file.open": "Open file action",
    "menu_file.save": "Save file action",
    "menu_file.exit": "Exit application action",
    
    # Edit Menu (2 keys)
    "menu_edit.undo": "Undo action",
    "menu_edit.redo": "Redo action",
    
    # View Menu (2 keys)
    "menu_view.theme_light": "Light theme",
    "menu_view.theme_dark": "Dark theme",
    
    # Tools Menu (11 keys)
    "menu_tools.cockpit": "Cockpit tool",
    "menu_tools.media": "Media tool",
    "menu_tools.tabs": "Tabs tool",
    "menu_tools.add_widget": "Add widget action",
    "menu_tools.system_monitor": "System monitor",
    "menu_tools.clock": "World clock",
    "menu_tools.network_traffic": "Network traffic",
    "menu_tools.gpu_monitor": "GPU monitor",
    "menu_tools.temperature": "Temperature",
    "menu_tools.disk_io": "Disk I/O",
    "menu_tools.media_controls": "Media controls",
    
    # Dialogs - About (5 keys)
    "dialogs.about.title": "About dialog title",
    "dialogs.about.version": "Version string",
    "dialogs.about.description": "Application description",
    "dialogs.about.copyright": "Copyright notice",
    "dialogs.about.license": "License information",
    
    # Tabs (2 keys)
    "tabs.cockpit": "Cockpit tab",
    "tabs.media_commander": "Media Commander tab",
    
    # Widget Selector Dialog (7 keys)
    "dialogs.widget_selector.title": "Widget selector title",
    "dialogs.widget_selector.preview": "Preview label",
    "dialogs.widget_selector.size_select": "Size selection label",
    "dialogs.widget_selector.add_button": "Add button text",
    "dialogs.widget_selector.scale": "Scale label",
    "dialogs.widget_selector.error": "Error message"
}

def extract_english_values():
    """Extract English values for all critical keys."""
    base_path = Path("i18n/translations")
    en_file = base_path / "en.json"
    
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    extracted = {}
    
    for key_path, description in CRITICAL_KEYS.items():
        # Navigate nested structure
        keys = key_path.split(".")
        value = en_data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                value = None
                break
        
        if value and isinstance(value, str):
            extracted[key_path] = {
                "en": value,
                "description": description
            }
        else:
            print(f"⚠️  Key not found: {key_path}")
    
    return extracted

def get_german_reference():
    """Get German translations as reference for quality."""
    base_path = Path("i18n/translations")
    de_file = base_path / "de.json"
    
    with open(de_file, 'r', encoding='utf-8') as f:
        de_data = json.load(f)
    
    extracted = {}
    
    for key_path in CRITICAL_KEYS.keys():
        keys = key_path.split(".")
        value = de_data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                value = None
                break
        
        if value and isinstance(value, str):
            extracted[key_path] = value
    
    return extracted

def create_translation_template():
    """Creates a translation template showing EN + DE for reference."""
    english_values = extract_english_values()
    german_values = get_german_reference()
    
    print("="*80)
    print("TRANSLATION TEMPLATE - Tier 1 Languages (7)")
    print("="*80)
    print(f"\nLanguages: {', '.join(TIER_1_LANGUAGES.values())}")
    print(f"Critical Keys: {len(CRITICAL_KEYS)}")
    print(f"Total Translations Needed: {len(TIER_1_LANGUAGES)} × {len(CRITICAL_KEYS)} = {len(TIER_1_LANGUAGES) * len(CRITICAL_KEYS)}")
    print("\n" + "="*80)
    print("REFERENCE TRANSLATIONS (EN → DE)")
    print("="*80 + "\n")
    
    for key_path, data in english_values.items():
        de_value = german_values.get(key_path, "N/A")
        print(f"Key: {key_path}")
        print(f"  EN: {data['en']}")
        print(f"  DE: {de_value}")
        print(f"  Description: {data['description']}")
        print()
    
    # Save to file for reference
    output = {
        "metadata": {
            "tier": 1,
            "languages": TIER_1_LANGUAGES,
            "total_keys": len(CRITICAL_KEYS),
            "total_translations": len(TIER_1_LANGUAGES) * len(CRITICAL_KEYS)
        },
        "translations": {}
    }
    
    for key_path, data in english_values.items():
        output["translations"][key_path] = {
            "en": data["en"],
            "de": german_values.get(key_path, "N/A"),
            "description": data["description"],
            "languages": {lang_code: "" for lang_code in TIER_1_LANGUAGES.keys()}
        }
    
    with open("translation_template_tier1.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("="*80)
    print("✅ Template saved to: translation_template_tier1.json")
    print("="*80)

if __name__ == "__main__":
    os.chdir("c:/Dev/Repos/JanFriske/MacGyver Multi-Tool")
    create_translation_template()
