import json
import os
import shutil

# Define the 17 new languages to add
NEW_LANGUAGES = [
    # Tier 1 - Critical
    ("ps", "Pashto (Afghan)"),
    ("fa-AF", "Dari (Afghan Persian)"),
    ("ko", "Korean"),
    ("id", "Indonesian"),
    ("th", "Thai"),
    ("bn", "Bengali"),
    ("ur", "Urdu"),
    # Tier 2 - Important
    ("ta", "Tamil"),
    ("te", "Telugu"),
    ("mr", "Marathi"),
    ("uk", "Ukrainian"),
    ("ms", "Malay"),
    # Tier 3 - Useful
    ("el", "Greek"),
    ("ca", "Catalan"),
    ("eu", "Basque"),
    ("gl", "Galician"),
    ("fa", "Persian (Farsi)")
]

def create_language_files():
    """Create JSON files for 17 new languages based on en.json template."""
    
    base_path = "i18n/translations"
    en_file = os.path.join(base_path, "en.json")
    
    # Load English template
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    created_count = 0
    skipped_count = 0
    
    for lang_code, lang_name in NEW_LANGUAGES:
        # Handle special case: fa-AF becomes fa_AF for filename
        filename = lang_code.replace('-', '_') + '.json'
        target_file = os.path.join(base_path, filename)
        
        # Skip if already exists
        if os.path.exists(target_file):
            print(f"⏭️  {lang_code:8s} - {lang_name:30s} [SKIPPED - already exists]")
            skipped_count += 1
            continue
        
        # Create new file with English content
        # (will be translated by update_tooltips.py later)
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(en_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ {lang_code:8s} - {lang_name:30s} [CREATED]")
        created_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Created: {created_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total:   {len(NEW_LANGUAGES)}")
    print(f"{'='*60}")
    print(f"\n✅ Next step: Run 'update_tooltips.py' to add German tooltips to all files!")

if __name__ == "__main__":
    create_language_files()
