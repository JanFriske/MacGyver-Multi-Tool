"""
Convert all SVG flags to PNG format for reliable Qt display.

Qt's SVG renderer has issues with certain SVG features. Converting to PNG
ensures all flags display correctly.
"""

from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
import sys

# Initialize Qt application
app = QApplication(sys.argv)

# Paths
svg_dir = Path("assets/flags")
output_dir = svg_dir

# Target size (4:3 ratio) - increased for better visibility
WIDTH = 40
HEIGHT = 30

print("=" * 70)
print("SVG to PNG Converter for Flag Icons")
print("=" * 70)

# Get all SVG files
svg_files = list(svg_dir.glob("*.svg"))
print(f"\nFound {len(svg_files)} SVG files")

converted = 0
failed = 0
skipped = 0

for svg_file in sorted(svg_files):
    png_file = output_dir / f"{svg_file.stem}.png"
    
    # Skip if PNG already exists and is newer
    if png_file.exists() and png_file.stat().st_mtime > svg_file.stat().st_mtime:
        skipped += 1
        continue
    
    try:
        # Load SVG
        renderer = QSvgRenderer(str(svg_file))
        
        if not renderer.isValid():
            print(f"❌ {svg_file.name}: Invalid SVG")
            failed += 1
            continue
        
        # Create pixmap
        pixmap = QPixmap(WIDTH, HEIGHT)
        pixmap.fill(Qt.transparent)
        
        # Render SVG to pixmap
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Save as PNG
        if pixmap.save(str(png_file), "PNG"):
            print(f"✅ {svg_file.stem}.svg → {svg_file.stem}.png")
            converted += 1
        else:
            print(f"❌ {svg_file.name}: Failed to save PNG")
            failed += 1
            
    except Exception as e:
        print(f"❌ {svg_file.name}: {e}")
        failed += 1

print("\n" + "=" * 70)
print("Summary:")
print(f"  ✅ Converted: {converted}")
print(f"  ⏭️  Skipped (up-to-date): {skipped}")
print(f"  ❌ Failed: {failed}")
print(f"  📁 Total PNG files: {len(list(output_dir.glob('*.png')))}")
print("=" * 70)
