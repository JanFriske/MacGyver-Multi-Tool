"""
Download ALL required SVG flags from flag-icon-css repository.

This script reads i18n/flags.json and downloads ALL corresponding SVG files
from the flag-icon-css GitHub repository to assets/flags/.
"""

import json
import requests
from pathlib import Path
from typing import Dict, Set
import time

# Base URL for flag-icon-css SVG files (4x3 ratio)
FLAG_ICON_BASE_URL = "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{code}.svg"

# Fallback for special flags
SPECIAL_FLAGS = {
    "gb-sct": "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb-sct.svg",
    "gb-wls": "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/gb-wls.svg",
    "es-ct": "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es-ct.svg",
    "es-ga": "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es-ga.svg",
    "es-pv": "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es-pv.svg",
    "es-vc": "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/es-vc.svg",
    "un": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Flag_of_the_United_Nations.svg",
}


def load_flags_mapping() -> Dict[str, str]:
    """Load the flags.json mapping file."""
    flags_json_path = Path(__file__).parent.parent / "i18n" / "flags.json"
    
    if not flags_json_path.exists():
        raise FileNotFoundError(f"flags.json not found at {flags_json_path}")
    
    with open(flags_json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_needed_country_codes(flags_mapping: Dict[str, str]) -> Set[str]:
    """Extract unique country codes from flags mapping."""
    return set(flags_mapping.values())


def download_flag(country_code: str, output_path: Path) -> bool:
    """
    Download a single flag SVG.
    
    Args:
        country_code: ISO country code or special code
        output_path: Path where the SVG should be saved
    
    Returns:
        True if successful, False otherwise
    """
    # Check for special flags first
    if country_code in SPECIAL_FLAGS:
        url = SPECIAL_FLAGS[country_code]
    else:
        url = FLAG_ICON_BASE_URL.format(code=country_code)
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Verify it's SVG content
        content = response.text
        if not content.strip().startswith("<?xml") and not content.strip().startswith("<svg"):
            print(f"   ⚠️  Warning: {country_code} - Response doesn't appear to be SVG")
            return False
        
        # Save to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed: {str(e)[:50]}")
        return False


def main():
    """Main function to download all required flag SVGs."""
    print("🏁 Complete Flag SVG Download Script")
    print("=" * 70)
    
    # Load flags mapping
    print("\n📖 Loading flags.json...")
    try:
        flags_mapping = load_flags_mapping()
        print(f"   ✅ Found {len(flags_mapping)} language entries")
    except Exception as e:
        print(f"   ❌ Error loading flags.json: {e}")
        return
    
    # Get needed country codes
    needed_codes = get_needed_country_codes(flags_mapping)
    print(f"   📊 Need {len(needed_codes)} unique country flags")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "assets" / "flags"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output directory: {output_dir}")
    
    # Check existing files
    existing_svgs = {f.stem for f in output_dir.glob("*.svg")}
    missing_codes = needed_codes - existing_svgs
    
    print(f"\n📊 Status:")
    print(f"   ✅ Already have: {len(existing_svgs)} flags")
    print(f"   ⬇️  Need to download: {len(missing_codes)} flags")
    
    if not missing_codes:
        print("\n✨ All flags already downloaded!")
        return
    
    # Download missing flags
    print("\n⬇️  Downloading missing SVG flags...")
    print("-" * 70)
    
    downloaded = 0
    failed = 0
    failed_codes = []
    
    for i, country_code in enumerate(sorted(missing_codes), 1):
        output_path = output_dir / f"{country_code}.svg"
        
        print(f"[{i}/{len(missing_codes)}] {country_code}.svg...", end=" ", flush=True)
        
        if download_flag(country_code, output_path):
            print("✅")
            downloaded += 1
        else:
            failed += 1
            failed_codes.append(country_code)
        
        # Small delay to avoid rate limiting
        if i % 10 == 0:
            time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Download Summary:")
    print(f"   ✅ Successfully downloaded: {downloaded}")
    print(f"   ❌ Failed: {failed}")
    if failed_codes:
        print(f"   Failed codes: {', '.join(failed_codes)}")
    
    total_svgs = len(list(output_dir.glob("*.svg")))
    print(f"\n   📁 Total SVG files now: {total_svgs}/{len(needed_codes)}")
    
    if total_svgs == len(needed_codes):
        print("\n✨ SUCCESS! All required flags downloaded!")
    else:
        print(f"\n⚠️  Still missing {len(needed_codes) - total_svgs} flags")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
