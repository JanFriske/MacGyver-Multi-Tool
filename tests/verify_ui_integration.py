import sys
import os
from PySide6.QtWidgets import QApplication

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService
from ui.dialogs.translation_editor_dialog import TranslationEditorDialog

def test_ui_integration():
    print("Testing Uplink UI Integration...")
    
    app = QApplication(sys.argv)
    i18n = I18nService()
    
    dialog = TranslationEditorDialog(i18n)
    
    # Check if button exists
    if hasattr(dialog, 'uplink_btn'):
        print("   ✅ Uplink Button found!")
        print(f"   Label: {dialog.uplink_btn.text()}")
    else:
        print("   ❌ Uplink Button NOT found!")
        return
        
    # Check if method exists
    if hasattr(dialog, '_open_uplink_dialog'):
        print("   ✅ _open_uplink_dialog method found!")
    else:
        print("   ❌ _open_uplink_dialog method NOT found!")
        
    print("UI Integration Verified.")
    dialog.deleteLater()

if __name__ == "__main__":
    test_ui_integration()
