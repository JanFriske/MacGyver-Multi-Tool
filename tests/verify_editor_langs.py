import sys
import os
from PySide6.QtWidgets import QApplication, QComboBox

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService
from ui.dialogs.translation_editor_dialog import TranslationEditorDialog

def test_editor_languages():
    print("Testing Translation Editor Language List...")
    
    app = QApplication(sys.argv)
    
    # Setup Service
    i18n = I18nService()
    
    # Ensure custom language exists for test
    if "custom_esperanto" not in i18n.get_custom_languages():
        print("⚠️ 'custom_esperanto' not found in service. Creating mock entry...")
        i18n.custom_languages["custom_esperanto"] = {"language_name": "Esperanto"}
    
    # Create Dialog
    dialog = TranslationEditorDialog(i18n)
    
    # Check Combo Box Items
    combo = dialog.lang_combo
    found_custom = False
    
    print(f"Found {combo.count()} items in combo box.")
    
    for i in range(combo.count()):
        text = combo.itemText(i)
        data = combo.itemData(i)
        
        if data == "custom_esperanto":
            print(f"   ✅ Found Custom Language: '{text}' (Data: {data})")
            found_custom = True
            
    if found_custom:
        print("✅ Custom language verification passed!")
    else:
        print("❌ Custom language NOT found in combo box!")
        
    dialog.deleteLater()

if __name__ == "__main__":
    test_editor_languages()
