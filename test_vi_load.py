import json
import os

path = "c:/Dev/Repos/JanFriske/MacGyver Multi-Tool/i18n/translations/vi.json"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Raw loaded value for menu.file: {data['menu']['file']}")
print(f"Type: {type(data['menu']['file'])}")

# Check if it contains literal backslash
if "\\" in data['menu']['file']:
    print("WARNING: String contains literal backslash!")
else:
    print("String is clean.")
