"""Test if QIcon can load PNG files"""
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from pathlib import Path
import sys

app = QApplication(sys.argv)

test_files = ['de.png', 'fr.png', 'es.png', 'gb.png', 'us.png']

print("Testing QIcon PNG loading:")
print("=" * 50)

for filename in test_files:
    filepath = Path("assets/flags") / filename
    exists = filepath.exists()
    
    if exists:
        icon = QIcon(str(filepath))
        is_null = icon.isNull()
        sizes = icon.availableSizes()
        
        print(f"{filename}:")
        print(f"  Exists: {exists}")
        print(f"  QIcon.isNull(): {is_null}")
        print(f"  Available sizes: {sizes}")
    else:
        print(f"{filename}: FILE NOT FOUND")

print("=" * 50)
