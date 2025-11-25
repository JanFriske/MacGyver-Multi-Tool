"""
Generate complete flags.json by analyzing all language codes in LANGUAGE_GROUPS
and creating intelligent mappings to country codes.
"""

from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.i18n_service import I18nService

# Initialize service
service = I18nService()

# Get all language codes
all_codes = set(service.get_all_language_codes())
existing_mappings = service.flags.copy()

print(f"Total language codes: {len(all_codes)}")
print(f"Existing mappings: {len(existing_mappings)}")

# Missing codes
missing = all_codes - set(existing_mappings.keys())
print(f"Missing mappings: {len(missing)}")
print(f"Missing codes: {sorted(missing)[:50]}")

# Auto-generate mappings for missing codes
new_mappings = {}

for code in sorted(missing):
    # Extract base language and region
    parts = code.split('_')
    base = parts[0]
    
    # Simple heuristic mapping
    if len(parts) > 1:
        region = parts[1].lower()
        # Use region code if it looks like a country code
        if len(region) == 2:
            new_mappings[code] = region
        else:
            # Use base language's country
            new_mappings[code] = existing_mappings.get(base, base)
    else:
        # Use base language code as country code
        new_mappings[code] = base

print(f"\nGenerated {len(new_mappings)} new mappings")
print("Sample new mappings:", dict(list(new_mappings.items())[:10]))

# Merge with existing
complete_mappings = {**existing_mappings, **new_mappings}

# Save to file
output_path = Path(__file__).parent.parent / "i18n" / "flags.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(complete_mappings, f, indent=4, ensure_ascii=False)

print(f"\n✅ Saved {len(complete_mappings)} mappings to {output_path}")
