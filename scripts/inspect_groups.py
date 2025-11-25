"""
Inspect runtime LANGUAGE_GROUPS for emojis
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from core.services.i18n_service import I18nService

service = I18nService()
groups = service.get_language_groups()

print("Checking LANGUAGE_GROUPS for emojis...")

found = False
def check_dict(d, path=""):
    global found
    for k, v in d.items():
        # Check key
        if any(ord(c) > 127 for c in k):
            # Keys are allowed to have emojis (group headers), but let's see
            pass
            
        if isinstance(v, dict):
            check_dict(v, f"{path}.{k}")
        elif isinstance(v, str):
            # Check value (this is the display name)
            # We specifically look for Regional Indicator Symbols (flags)
            if any(0x1F1E6 <= ord(c) <= 0x1F1FF for c in v):
                print(f"⚠️ FOUND FLAG EMOJI in {path}.{k}: {v}")
                found = True
            elif any(ord(c) > 127 for c in v):
                 print(f"ℹ️ Found other special char in {path}.{k}: {v}")

check_dict(groups)

if not found:
    print("✅ No flag emojis found in LANGUAGE_GROUPS values.")
else:
    print("❌ Found flag emojis! Normalization failed.")
