import sys
import os
from PySide6.QtWidgets import QApplication

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.services.i18n_service import I18nService
from ui.dialogs.translation_stats_dialog import TranslationStatsDialog
from ui.dialogs.translation_editor_dialog import TranslationEditorDialog

def test_stats():
    print("Testing Translation Statistics...")
    
    app = QApplication(sys.argv)
    i18n = I18nService()
    
    # 1. Test Service Method
    print("\n1. Testing Service Method...")
    stats = i18n.get_translation_stats()
    if stats:
        print(f"   ✅ Stats calculated for {len(stats)} languages.")
        # Check structure of first item
        first_lang = list(stats.keys())[0]
        data = stats[first_lang]
        print(f"   Sample ({first_lang}): {data}")
        
        if "percent" in data and "total_keys" in data:
             print("   ✅ Data structure valid.")
        else:
             print("   ❌ Invalid data structure.")
    else:
        print("   ❌ No stats returned.")
        
    # 2. Test Dialog Instantiation
    print("\n2. Testing Dialog Instantiation...")
    try:
        dialog = TranslationStatsDialog(i18n)
        print("   ✅ Dialog instantiated successfully.")
        dialog.deleteLater()
    except Exception as e:
        print(f"   ❌ Dialog instantiation failed: {e}")
        
    # 3. Test Editor Integration
    print("\n3. Testing Editor Integration...")
    editor = TranslationEditorDialog(i18n)
    if hasattr(editor, 'stats_btn'):
        print("   ✅ Stats button found in Editor.")
    else:
        print("   ❌ Stats button NOT found in Editor.")
    editor.deleteLater()
    
    print("\nStatistics Verification Complete.")

if __name__ == "__main__":
    test_stats()
