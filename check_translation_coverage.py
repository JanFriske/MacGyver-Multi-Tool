"""
Script to compare translation files with LANGUAGE_GROUPS assignments
"""
import json
from pathlib import Path

# Get all language codes from LANGUAGE_GROUPS in i18n_service.py
def extract_codes_from_language_groups():
    """Extract all language codes from LANGUAGE_GROUPS structure."""
    # Import the i18n_service to get LANGUAGE_GROUPS
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from core.services.i18n_service import I18nService
    
    service = I18nService()
    groups = service.LANGUAGE_GROUPS
    
    codes = set()
    
    def collect_codes(node):
        if isinstance(node, dict):
            # If all values are strings, it's a leaf dict containing codes
            if node and all(isinstance(v, str) for v in node.values()):
                codes.update(node.keys())
            else:
                # Recurse into nested dicts
                for v in node.values():
                    collect_codes(v)
    
    for category in groups.values():
        collect_codes(category)
    
    return codes

# Get all translation files
def get_translation_files():
    """Get all .json files from translations directory."""
    translations_dir = Path(__file__).parent / "i18n" / "translations"
    return {f.stem for f in translations_dir.glob("*.json")}

# Main comparison
def main():
    codes_in_groups = extract_codes_from_language_groups()
    translation_files = get_translation_files()
    
    # Find missing codes (files without group assignment)
    missing_in_groups = translation_files - codes_in_groups
    
    # Find extra codes (groups without translation files)
    missing_files = codes_in_groups - translation_files
    
    # Write report to file
    output_file = Path(__file__).parent / "translation_coverage_report.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"TRANSLATION COVERAGE REPORT\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Total translation files: {len(translation_files)}\n")
        f.write(f"Total codes in LANGUAGE_GROUPS: {len(codes_in_groups)}\n")
        f.write(f"\n{'='*60}\n")
        
        if missing_in_groups:
            f.write(f"\nMISSING IN LANGUAGE_GROUPS ({len(missing_in_groups)}):\n")
            f.write(f"{'='*60}\n")
            for code in sorted(missing_in_groups):
                f.write(f"  - {code}\n")
        else:
            f.write("\nAll translation files are assigned to LANGUAGE_GROUPS!\n")
        
        if missing_files:
            f.write(f"\nCODES IN GROUPS WITHOUT TRANSLATION FILES ({len(missing_files)}):\n")
            f.write(f"{'='*60}\n")
            for code in sorted(missing_files):
                f.write(f"  - {code}\n")
        else:
            f.write("\nAll codes in LANGUAGE_GROUPS have translation files!\n")
        
        f.write(f"\n{'='*60}\n")
        f.write(f"Summary: {len(codes_in_groups & translation_files)} codes properly matched\n")
    
    print(f"Report written to: {output_file}")

if __name__ == "__main__":
    main()
