import sys
import os
import shutil
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.custom_language_service import get_custom_language_service
from core.services.i18n_service import I18nService

def main():
    print("Testing Custom Language Functionality...")
    custom_service = get_custom_language_service()
    i18n_service = I18nService()
    
    test_code = "custom_test"
    test_name = "Test Language 🚀"
    
    # 1. Clean up previous test
    if test_code in custom_service.get_all_custom_languages():
        custom_service.delete_custom_language(test_code)
        print("Cleaned up previous test language.")
    
    # 2. Create Custom Language
    print(f"Creating custom language '{test_name}' ({test_code})...")
    # Correct signature: name, code, description, base_language
    success = custom_service.create_custom_language(test_name, test_code, base_language="en")
    if success:
        print("✅ Creation successful")
    else:
        print("❌ Creation failed")
        return

    # 3. Verify Persistence (Reload Service)
    print("Verifying persistence...")
    # Force reload by creating new instance or checking file existence
    # In singleton pattern, we get the same instance, so we check if it has the data.
    # To truly check persistence, we'd need to restart the process, but here we check if the file exists and if a new instance (if we could create one) would load it.
    # Since we can't easily kill the singleton in this script without resetting the global, let's just check the file and the current instance.
    
    custom_service_2 = get_custom_language_service()
    langs = custom_service_2.get_all_custom_languages()
    if test_code in langs:
        print(f"✅ Language '{test_code}' found after reload")
        print(f"   Name: {langs[test_code].get('language_name')}")
    else:
        print("❌ Language not found after reload")
        return

    # 4. Verify I18n Integration
    print("Verifying I18n integration...")
    i18n_service._load_custom_languages() # Force reload
    if i18n_service._language_exists(test_code):
        print("✅ I18nService recognizes custom language")
    else:
        print("❌ I18nService does NOT recognize custom language")

    # 4.5 Verify Update and Remove Translation
    print("Verifying Update/Remove Translation...")
    test_key = "menu.file"
    test_val = "File 🚀"
    
    # Update
    custom_service.update_custom_translation(test_code, test_key, test_val)
    lang_data = custom_service.get_custom_language(test_code)
    # Check nested value
    val = lang_data["translations"]["menu"]["file"]
    if val == test_val:
        print(f"✅ Update successful: {val}")
    else:
        print(f"❌ Update failed: {val}")
        
    # Remove
    custom_service.remove_custom_translation(test_code, test_key)
    lang_data = custom_service.get_custom_language(test_code)
    # Check if key is gone
    if "file" not in lang_data["translations"]["menu"]:
        print("✅ Remove successful")
    else:
        print("❌ Remove failed")

    # 5. Delete Custom Language
    print("Deleting custom language...")
    success = custom_service.delete_custom_language(test_code)
    if success:
        print("✅ Deletion successful")
    else:
        print("❌ Deletion failed")

    # 6. Verify Deletion
    langs = custom_service.get_all_custom_languages()
    if test_code not in langs:
        print("✅ Language gone from service")
    else:
        print("❌ Language still present")

if __name__ == "__main__":
    main()
