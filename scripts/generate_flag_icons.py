"""
Generates PNG flag icons from emoji definitions in i18n/flags.json.
Saves to assets/flags/{code}.png

Run:
    python scripts/generate_flag_icons.py

This script uses PySide6 for reliable emoji rendering.
"""
from pathlib import Path
import json
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt

HERE = Path(__file__).parent.parent
ASSETS_DIR = HERE / "assets" / "flags"
FLAGS_JSON = HERE / "i18n" / "flags.json"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

if not FLAGS_JSON.exists():
    print(f"flags.json not found at {FLAGS_JSON}")
    sys.exit(1)

with open(FLAGS_JSON, "r", encoding="utf-8") as f:
    flags = json.load(f)

app = QApplication([])

def render_emoji_to_png(emoji: str, size: int = 64, out_path: Path = None):
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    font = QFont("Segoe UI Emoji", max(10, int(size * 0.6)))
    painter.setFont(font)
    painter.setPen(Qt.black)
    rect = pix.rect()
    painter.drawText(rect, Qt.AlignCenter, emoji)
    painter.end()
    if out_path:
        pix.save(str(out_path), "PNG")

count = 0
for code, emoji in flags.items():
    out = ASSETS_DIR / f"{code}.png"
    if out.exists():
        # skip existing
        continue
    try:
        render_emoji_to_png(emoji, size=48, out_path=out)
        count += 1
    except Exception as e:
        print(f"Failed to render {code}: {e}")

print(f"Generated {count} flag images in {ASSETS_DIR}")
app.quit()
