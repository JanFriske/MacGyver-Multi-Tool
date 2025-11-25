"""
Script to replace LANGUAGE_GROUPS in i18n_service.py with proper indentation
"""
from pathlib import Path

# Read the new structure
new_structure_file = Path("scripts/new_language_groups_structure.py")
with open(new_structure_file, 'r', encoding='utf-8') as f:
    new_structure_content = f.read()

# Extract just the LANGUAGE_GROUPS dict (skip comment lines)
lines = new_structure_content.split('\n')
start_idx = [i for i, l in enumerate(lines) if 'LANGUAGE_GROUPS = {' in l][0]
new_lang_groups_lines = lines[start_idx:]

# Add 4-space indentation to all lines (class-level variable)
indented_lines = []
for line in new_lang_groups_lines:
    if line:  # Only indent non-empty lines
        indented_lines.append('    ' + line)
    else:
        indented_lines.append(line)

# Read the existing i18n_service.py backup
service_file  = Path("core/services/i18n_service.py.backup")
with open(service_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
start = None
end = None

for i, line in enumerate(lines):
    if '    LANGUAGE_GROUPS = {' in line:
        start = i
    if start is not None and line.strip() == '}':
        # Check the indentation
        if len(line) - len(line.lstrip()) == 4:  # Class-level closing brace
            end = i
            break

if start is None or end is None:
    print(f"❌ Could not find LANGUAGE_GROUPS boundaries")
    exit(1)

print(f"Found LANGUAGE_GROUPS at lines {start+1} to {end+1}")
print(f"Replacing {end - start + 1} lines...")

# Replace
new_lines = (
    lines[:start] +  # Everything before
    indented_lines +  # New LANGUAGE_GROUPS (indented)
    lines[end+1:]  # Everything after
)

# Write to the actual file (not backup)
output_file = Path("core/services/i18n_service.py")
new_content = '\n'.join(new_lines)
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Successfully replaced LANGUAGE_GROUPS structure!")
print(f"✅ File saved: {output_file}")
print(f"\n📊 New structure:")
print(f"   - 6 Geographic Categories")
print(f"   - 3 Special Categories")
print(f"   - ☠️ Icons for Pirate variants")
print(f"   - 🇩🇪 🇬🇧 🇫🇷 National flag emojis")
