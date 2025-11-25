from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Add project root to sys.path so imports work when running this script directly
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Ensure menu icons are allowed
attr = getattr(Qt, 'AA_DontShowIconsInMenus', None)
if attr is not None:
    QApplication.setAttribute(attr, False)

from ui.view import MainWindow
from presenter.controller import Controller

app = QApplication(sys.argv)
win = MainWindow()
ctrl = Controller(win)

codes = ['en','en_GB','en_US','gd','sco']
for code in codes:
    a = win.language_actions.get(code)
    print(code, 'action_exists=', a is not None)
    if a:
        print(' has_icon=', not a.icon().isNull(), 'text=', a.text())

# Close app
app.quit()
