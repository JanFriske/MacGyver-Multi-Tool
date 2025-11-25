import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.custom_language_service import get_custom_language_service

def main():
    print("Testing Custom Language Import/Export...")
    service = get_custom_language_service()
    
    # 1. Create a source language
    src_code = "custom_export_test"
    src_name = "Export Test Language"
    
    if src_code in service.get_all_custom_languages():
        service.delete_custom_language(src_code)
        
    service.create_custom_language(src_name, src_code, base_language="en")
    service.update_custom_translation(src_code, "menu.file", "File Exported")
    
    # 2. Export
    print("Exporting...")
    export_data = service.export_custom_language(src_code)
    
    if export_data["language_code"] == src_code:
        print("✅ Export data has correct code")
    else:
        print("❌ Export data has wrong code")
        
    if "menu.file" in export_data["translations"]:
        print("✅ Export data has translation (flat)")
    else:
        print("❌ Export data missing translation")
        
    # 3. Import as new language
    print("Importing as new language...")
    new_code = "custom_import_test"
    
    # Modify export data to look like a new language
    export_data["language_code"] = new_code
    export_data["language_name"] = "Import Test Language"
    
    if new_code in service.get_all_custom_languages():
        service.delete_custom_language(new_code)
        
    imported_code = service.import_custom_language(export_data)
    
    if imported_code == new_code:
        print(f"✅ Imported code matches: {imported_code}")
    else:
        print(f"❌ Imported code mismatch: {imported_code}")
        
    # Verify content
    lang_data = service.get_custom_language(new_code)
    val = lang_data["translations"]["menu"]["file"]
    if val == "File Exported":
        print("✅ Imported translation matches")
    else:
        print(f"❌ Imported translation mismatch: {val}")
        
    # Cleanup
    service.delete_custom_language(src_code)
    service.delete_custom_language(new_code)
    print("Cleanup complete.")

if __name__ == "__main__":
    main()
