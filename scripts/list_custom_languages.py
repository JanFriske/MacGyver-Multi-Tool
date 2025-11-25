import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.custom_language_service import CustomLanguageService

def main():
    print("Checking custom languages...")
    service = CustomLanguageService()
    langs = service.get_all_custom_languages()
    
    print(f"Found {len(langs)} custom languages:")
    for code, data in langs.items():
        print(f" - {code}: {data.get('language_name')} (File: {service.custom_dir / f'{code}.json'})")
        
    print(f"\nCustom Directory: {service.custom_dir}")
    if service.custom_dir.exists():
        print("Directory exists.")
        print("Contents:")
        for f in service.custom_dir.iterdir():
            print(f"  - {f.name}")
    else:
        print("Directory does NOT exist.")

    # Try creating a test language
    print("\nAttempting to create 'custom_test_script'...")
    try:
        service.create_custom_language("Test Script", "test_script", "Created by script")
        print("Creation successful.")
    except Exception as e:
        print(f"Creation FAILED: {e}")

    # Delete the test language
    print("\nDeleting 'custom_test_script'...")
    try:
        if service.delete_custom_language("custom_test_script"):
            print("Deletion successful.")
        else:
            print("Deletion failed (not found).")
    except Exception as e:
        print(f"Deletion error: {e}")

    # Final check
    print("\nFinal check...")
    langs = service.get_all_custom_languages()
    print(f"Found {len(langs)} custom languages.")

if __name__ == "__main__":
    main()
