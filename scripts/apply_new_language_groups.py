"""
Script to replace LANGUAGE_GROUPS in i18n_service.py
with the new geographic structure
"""
from pathlib import Path

# Read the new structure
new_structure_file = Path("scripts/new_language_groups_structure.py")
with open(new_structure_file, 'r', encoding='utf-8') as f:
    new_structure = f.read()

# Extract just the LANGUAGE_GROUPS dict (skip the comment lines at the top)
lines = new_structure.split('\n')
start_idx = [i for i, l in enumerate(lines) if 'LANGUAGE_GROUPS = {' in l][0]
new_lang_groups = '\n'.join(lines[start_idx:])

# Read the existing i18n_service.py
service_file = Path("core/services/i18n_service.py")
with open(service_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find start and end of LANGUAGE_GROUPS
lines = content.split('\n')
start = None
end = None

for i, line in enumerate(lines):
    if 'LANGUAGE_GROUPS = {' in line:
        start = i
    if start is not None and line.strip() == '}' and i > start + 10:
        # Check if this is the closing brace for LANGUAGE_GROUPS
        indent_count = len(line) - len(line.lstrip())
        if indent_count == 4:  # Class-level closing brace
            end = i
            break

if start is None or end is None:
    print(f"❌ Could not find LANGUAGE_GROUPS boundaries")
    print(f"Start: {start}, End: {end}")
    exit(1)

print(f"Found LANGUAGE_GROUPS at lines {start+1} to {end+1}")
print(f"Replacing {end - start + 1} lines...")

# Replace the old structure with the new one
new_lines = (
    lines[:start] +  # Everything before LANGUAGE_GROUPS
    new_lang_groups.split('\n') +  # New LANGUAGE_GROUPS
    lines[end+1:]  # Everything after old LANGUAGE_GROUPS
)

# Write back
new_content = '\n'.join(new_lines)
with open(service_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Successfully replaced LANGUAGE_GROUPS structure!")
print(f"✅ File saved: {service_file}")
print(f"\n📊 New structure:")
print(f"   - 6 Geographic Categories (Afrika, Asien, Europa, N/S-Amerika, Ozeanien)")
print(f"   - 3 Special Categories (Klassisch & Konstruiert, Historisch & Spezial, Deutsche Dialekte)")
print(f"   - ☠️ Icons for Pirate variants")
print(f"   - National flag emojis for countries")
