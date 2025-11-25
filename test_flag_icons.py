"""Debug script to test flag icon loading"""
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from pathlib import Path
from core.services.i18n_service import I18nService
import sys

app = QApplication(sys.argv)

# Test i18n service
print("=" * 70)
print("Testing I18nService flag loading")
print("=" * 70)

service = I18nService()

test_codes = ['de', 'en', 'fr', 'es', 'it', 'pl', 'el', 'ru']

for code in test_codes:
    flag_path = service.get_flag_path(code)
    print(f"\n{code}:")
    print(f"  Path: {flag_path}")
    print(f"  Exists: {flag_path.exists() if flag_path else False}")
    
    if flag_path and flag_path.exists():
        # Test QIcon loading
        icon = QIcon(str(flag_path))
        print(f"  QIcon null: {icon.isNull()}")
        print(f"  QIcon available sizes: {icon.availableSizes()}")
        
        # Try to get pixmap
        pixmap = icon.pixmap(20, 15)
        print(f"  Pixmap null: {pixmap.isNull()}")
        print(f"  Pixmap size: {pixmap.width()}x{pixmap.height()}")

print("\n" + "=" * 70)
print("Summary:")
print("=" * 70)
print(f"Total flags in flags.json: {len(service.flags)}")
print(f"SVG files in assets/flags: {len(list(Path('assets/flags').glob('*.svg')))}")
