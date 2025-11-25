from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import QObject, Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

# i18n Services
from core.services.i18n_service import I18nService
from core.services.language_manager import LanguageManager

class Controller(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.view.tool_opened.connect(self.handle_tool_opened)
        self.view.theme_changed.connect(self.change_theme)
        
        # i18n Setup
        self.i18n_service = I18nService()
        self.language_manager = LanguageManager(self.i18n_service)
        self.language_manager.language_changed.connect(self._on_language_changed)
        self.view.language_changed.connect(self.language_manager.set_language)
        self.view.delete_custom_language_requested.connect(self._handle_delete_custom_language)
        
        # Setze i18n Service im View
        self.view.set_i18n_service(self.i18n_service)
        
        # Setze initiale Sprache im View
        current_lang = self.language_manager.get_current_language()
        self.view.set_current_language(current_lang)

        # Central Media Player Instance
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
    
    def _on_language_changed(self, lang_code: str):
        """Wird aufgerufen wenn die Sprache geändert wird."""
        # Aktualisiere alle UI-Elemente
        self.view.update_ui_language()

    def _handle_delete_custom_language(self, lang_code: str):
        """Handles the request to delete a custom language."""
        from PySide6.QtWidgets import QMessageBox
        
        # Confirm
        msg = QMessageBox(self.view)
        msg.setWindowTitle(self.view.tr("dialog.delete_lang_title", "Sprache löschen"))
        msg.setText(self.view.tr("dialog.delete_lang_confirm", "Möchten Sie diese Sprache wirklich löschen?"))
        msg.setInformativeText(f"Code: {lang_code}")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        if msg.exec() == QMessageBox.Yes:
            if self.i18n_service.delete_custom_language(lang_code):
                # Refresh UI
                self.view.refresh_language_menu()
                
                # If deleted language was active, switch to default
                if self.language_manager.get_current_language() == lang_code:
                    self.language_manager.set_language("en")
            else:
                QMessageBox.warning(self.view, "Fehler", "Konnte Sprache nicht löschen.")

    def handle_tool_opened(self, tool_name):
        # Widget Selector
        if tool_name == "add_widget":
            self._show_widget_selector()
            return

        # Cockpit Tools (Dashboard Integration)
        if tool_name in ["system_info", "clock", "network_monitor", "gpu_monitor", "temp_monitor", "disk_monitor"]:
            # Ensure Cockpit Dashboard exists
            self.view._ensure_cockpit_dashboard()
            
            widget = None
            if tool_name == "system_info":
                widget = self._create_system_monitor()
            elif tool_name == "clock":
                widget = self._create_clock()
            elif tool_name == "network_monitor":
                widget = self._create_network_monitor()
            elif tool_name == "gpu_monitor":
                widget = self._create_gpu_monitor()
            elif tool_name == "temp_monitor":
                widget = self._create_temp_monitor()
            elif tool_name == "disk_monitor":
                widget = self._create_disk_monitor()
            
            if widget:
                # Add to Dashboard
                # Use span from widget if available (MacGyverWidget has span_w/h)
                span_w = getattr(widget, 'span_w', 1)
                span_h = getattr(widget, 'span_h', 1)
                self.view.cockpit_dashboard.add_widget(widget, span_w, span_h)
                self.view.main_tab_widget.setCurrentWidget(self.view.cockpit_tab)
        
        # Media Tools
        elif tool_name == "media_controls":
            widget = self._create_media_controls()
            self.view.add_tool_tab("Medien-Steuerung", widget, target="media")
        elif tool_name == "video_screen":
            widget = self._create_video_screen()
            self.view.add_tool_tab("Video-Screen", widget, target="media")
        elif tool_name == "media_explorer":
            widget = self._create_media_explorer()
            self.view.add_tool_tab("Medien-Explorer", widget, target="media")
        elif tool_name == "stream_window":
            widget = self._create_stream_widget()
            self.view.add_tool_tab("Online Stream", widget, target="media")
        elif tool_name == "equalizer":
            widget = self._create_equalizer_widget()
            self.view.add_tool_tab("Equalizer", widget, target="media")
            
        # Main Tabs
        elif tool_name == "file_manager":
            widget = self._create_file_manager_widget()
            self.view.add_tool_tab("Dateiverwaltung", widget, target="tab")
        elif tool_name == "network_diag":
            widget = self._create_network_diag_widget()
            self.view.add_tool_tab("Netzwerkdiagnose", widget, target="tab")

    def _show_widget_selector(self):
        from ui.tools.widget_selector import WidgetSelectorDialog
        dialog = WidgetSelectorDialog(self.view)
        dialog.widget_selected.connect(self._add_widget_from_selector)
        dialog.exec()

    def _add_widget_from_selector(self, widget_class, span_w, span_h):
        self.view._ensure_cockpit_dashboard()
        
        # Create instance
        widget = widget_class()
        
        # CRITICAL: We must explicitly rebuild the widget for the requested span
        # otherwise it stays at its default size (usually 2x1 or 1x1)
        if hasattr(widget, 'rebuild_for_span'):
            widget.rebuild_for_span(span_w, span_h)
        else:
            # Fallback for non-MacGyver widgets (shouldn't happen)
            widget.span_w = span_w
            widget.span_h = span_h
        
        self.view.cockpit_dashboard.add_widget(widget, span_w, span_h)
        self.view.main_tab_widget.setCurrentWidget(self.view.cockpit_tab)

    def change_theme(self, theme):
        if theme == "dark":
            try:
                with open("ui/styles/mac_dark.qss", "r") as f:
                    self.view.setStyleSheet(f.read())
            except FileNotFoundError:
                print("Error: mac_dark.qss not found.")
        else:
            try:
                with open("ui/styles/mac_light.qss", "r") as f:
                    self.view.setStyleSheet(f.read())
            except FileNotFoundError:
                print("Error: mac_light.qss not found.")

    # --- Cockpit Werkzeuge ---
    def _create_system_monitor(self):
        from ui.tools.gadgets import SystemMonitorWidget
        return SystemMonitorWidget()

    def _create_clock(self):
        from ui.tools.gadgets import ClockWidget
        return ClockWidget()

    def _create_network_monitor(self):
        from ui.tools.gadgets import NetworkMonitorWidget
        return NetworkMonitorWidget()

    def _create_gpu_monitor(self):
        from ui.tools.gadgets import GPUMonitorWidget
        return GPUMonitorWidget()

    def _create_temp_monitor(self):
        from ui.tools.gadgets import TempMonitorWidget
        return TempMonitorWidget()

    def _create_disk_monitor(self):
        from ui.tools.gadgets import DiskIOMonitorWidget
        return DiskIOMonitorWidget()

    # --- Legacy / Placeholder Werkzeuge ---
    def _create_system_info_widget(self):
        # Fallback if needed
        from ui.tools.system_info import SystemInfoWidget
        return SystemInfoWidget()

    def _create_file_manager_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🗂️ Dateiverwaltung (Stub-Modul)"))
        layout.addWidget(QLabel("Hier könnte eine Dateiansicht erscheinen."))
        widget.setLayout(layout)
        return widget

    def _create_network_diag_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🌐 Netzwerkdiagnose"))
        layout.addWidget(QLabel("Hier könnten Ping- und Traceroute-Tools laufen."))
        widget.setLayout(layout)
        return widget

    # --- Media Werkzeuge ---
    def _create_media_controls(self):
        from ui.tools.media_controls import MediaControlWidget
        return MediaControlWidget(self.media_player, self.audio_output)

    def _create_video_screen(self):
        from ui.tools.video_screen import VideoScreenWidget
        return VideoScreenWidget(self.media_player)

    def _create_media_explorer(self):
        from ui.tools.media_explorer import MediaExplorerWidget
        widget = MediaExplorerWidget()
        # Connect file selection to player
        widget.file_selected.connect(lambda path: self._play_media_file(path))
        return widget

    def _play_media_file(self, path):
        from PySide6.QtCore import QUrl
        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.media_player.play()

    def _create_stream_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📡 Online Stream"))
        layout.addWidget(QLabel("URL: [ http://... ] [Go]"))
        widget.setLayout(layout)
        return widget

    def _create_equalizer_widget(self):
        from ui.tools.equalizer import EqualizerWidget
        return EqualizerWidget()