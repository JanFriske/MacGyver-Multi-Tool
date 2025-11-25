import sys
import os
from PySide6.QtWidgets import QApplication

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_widgets():
    print("Testing Widget Instantiation...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    widgets_to_test = [
        ("ui.tools.gadgets", "ClockWidget"),
        ("ui.tools.gadgets", "SystemMonitorWidget"),
        ("ui.tools.gadgets", "NetworkMonitorWidget"),
        ("ui.tools.gadgets", "GPUMonitorWidget"),
        ("ui.tools.gadgets", "TempMonitorWidget"),
        ("ui.tools.gadgets", "DiskIOMonitorWidget"),
        ("ui.tools.network_widgets", "PingWidget"),
        ("ui.tools.network_widgets", "ConnectionStatusWidget"),
        ("ui.tools.network_widgets", "SpeedTestWidget"),
        ("ui.tools.network_widgets", "ActiveConnectionsWidget"),
        ("ui.tools.network_widgets", "NetworkPathWidget"),
        ("ui.tools.file_widgets", "DirectoryBrowserWidget"),
        ("ui.tools.file_widgets", "QuickAccessWidget"),
        ("ui.tools.file_widgets", "FileStatsWidget"),
        ("ui.tools.file_widgets", "RecentFilesWidget"),
        ("ui.tools.media_controls", "MediaControlWidget"),
        ("ui.tools.media_player", "MediaPlayerWidget"),
        ("ui.tools.equalizer", "EqualizerWidget"),
        ("ui.tools.video_screen", "VideoScreenWidget"),
        ("ui.tools.media_explorer", "MediaExplorerWidget"),
    ]
    
    success_count = 0
    fail_count = 0
    
    for module_name, class_name in widgets_to_test:
        try:
            # Import module
            module = __import__(module_name, fromlist=[class_name])
            # Get class
            widget_class = getattr(module, class_name)
            
            # Special handling for MediaControlWidget
            if class_name == "MediaControlWidget":
                from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
                player = QMediaPlayer()
                audio = QAudioOutput()
                widget = widget_class(player, audio)
            else:
                # Instantiate normally
                widget = widget_class()
                
            print(f"   ✅ Instantiated: {class_name}")
            success_count += 1
            
            # Clean up
            widget.deleteLater()
            
        except Exception as e:
            print(f"   ❌ Failed: {class_name} - {e}")
            fail_count += 1
            
    print(f"\nWidget Test Complete: {success_count} Passed, {fail_count} Failed")
    
    if fail_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_widgets()
