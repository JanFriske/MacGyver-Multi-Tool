from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QLabel, QPushButton, QWidget, QFrame, QListWidgetItem)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QColor, QPainter

from ui.components.macgyver_widget import MacGyverWidget
# Import gadgets for preview
from ui.tools.gadgets import (ClockWidget, SystemMonitorWidget, NetworkMonitorWidget, 
                              GPUMonitorWidget, TempMonitorWidget, DiskIOMonitorWidget)
from ui.tools.file_widgets import (DirectoryBrowserWidget, QuickAccessWidget,
                                   FileStatsWidget, RecentFilesWidget)
from ui.tools.network_widgets import (PingWidget, ConnectionStatusWidget,
                                      SpeedTestWidget, ActiveConnectionsWidget,
                                      NetworkPathWidget)

class WidgetSelectorDialog(QDialog):
    widget_selected = Signal(object, int, int) # widget_class, span_w, span_h

    def __init__(self, parent=None):
        super().__init__(parent)
        # Need to store parent to access i18n service if needed, or use global/singleton if available.
        # Assuming parent (MainWindow) has tr() method or we can use QCoreApplication.translate but we have a custom tr() in MainWindow.
        # Ideally we should pass the i18n service or use the parent's tr.
        # Since this is a dialog opened from MainWindow, parent should be set.
        self.main_window = parent
        
        self.setWindowTitle(self.tr("dialogs.widget_selector.title", "Widget hinzufügen"))
        self.setFixedSize(800, 500)
        self.setStyleSheet("""
            QDialog { background-color: #2d2d2d; color: white; }
            QListWidget { background-color: #1e1e1e; border: none; border-radius: 10px; padding: 10px; }
            QListWidget::item { padding: 10px; border-radius: 5px; color: #ddd; }
            QListWidget::item:selected { background-color: #007aff; color: white; }
            QLabel { color: #eee; font-family: 'Segoe UI'; }
            QPushButton {
                background-color: #3a3a3a; border: 1px solid #555; border-radius: 6px;
                padding: 8px 16px; color: white; font-weight: bold;
            }
            QPushButton:hover { background-color: #4a4a4a; }
            QPushButton:checked { background-color: #007aff; border-color: #007aff; }
        """)
        
        self.layout = QHBoxLayout(self)
        
        # Left: Widget List
        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(250)
        self.list_widget.currentRowChanged.connect(self._on_selection_changed)
        self.layout.addWidget(self.list_widget)
        
        # Right: Preview & Options
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.layout.addWidget(self.right_panel)
        
        # Preview Area
        self.preview_label = QLabel(self.tr("dialogs.widget_selector.preview", "Vorschau"))
        self.preview_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.right_layout.addWidget(self.preview_label)
        
        self.preview_container = QFrame()
        self.preview_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1a1a1a, stop:1 #252525);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        self.preview_container.setFixedSize(400, 300)
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.preview_container)
        
        # Size Options
        self.size_label = QLabel(self.tr("dialogs.widget_selector.size_select", "Größe wählen:"))
        self.size_label.setStyleSheet("margin-top: 20px;")
        self.right_layout.addWidget(self.size_label)
        
        # Size buttons container (will be repopulated per widget)
        self.size_buttons_layout = QHBoxLayout()
        self.size_buttons = []  # Track all size buttons
        self.right_layout.addLayout(self.size_buttons_layout)
        
        # Widget size restrictions (function-oriented)
        self.WIDGET_SIZES = {
            # System Monitoring
            'ClockWidget': [(2, 1), (3, 1), (3, 2), (3, 3)],
            'SystemMonitorWidget': [(2, 1), (2, 2)],
            'NetworkMonitorWidget': [(2, 1), (3, 1)],
            'GPUMonitorWidget': [(2, 1), (2, 2)],
            'TempMonitorWidget': [(1, 1), (2, 1)],
            'DiskIOMonitorWidget': [(2, 2), (4, 2)],
            
            # File Manager
            'DirectoryBrowserWidget': [(4, 2)],  # Full width only
            'QuickAccessWidget': [(1, 1), (2, 1)],
            'FileStatsWidget': [(1, 1), (2, 1)],
            'RecentFilesWidget': [(2, 1), (3, 1), (4, 1)],
            
            # Network Diagnostics
            'PingWidget': [(2, 1), (3, 1)],
            'ConnectionStatusWidget': [(1, 1), (2, 1)],
            'SpeedTestWidget': [(2, 1), (3, 1)],
            'ActiveConnectionsWidget': [(4, 2)],  # Full width only
            'NetworkPathWidget': [(3, 2), (4, 2)],
        }
        
        self.right_layout.addStretch()
        
        # Add Button
        self.add_btn = QPushButton(self.tr("dialogs.widget_selector.add_button", "Zum Dashboard hinzufügen"))
        self.add_btn.setStyleSheet("background-color: #34c759; border: none; padding: 12px;")
        self.add_btn.clicked.connect(self._add_widget)
        self.right_layout.addWidget(self.add_btn)
        
        # Default selection - MUST be before _populate_list()
        self.current_widget_class = None
        self.current_span = (2, 1)
        
        self._populate_list()

    def tr(self, key, default=None):
        if self.main_window and hasattr(self.main_window, 'tr'):
            return self.main_window.tr(key, default)
        return default if default else key

    def _populate_list(self):
        items = [
            # System Monitoring
            (f"⚙️ {self.tr('widgets.clock', 'Weltzeituhr')}", ClockWidget),
            (f"⚙️ {self.tr('widgets.system_monitor', 'System Monitor')}", SystemMonitorWidget),
            (f"⚙️ {self.tr('widgets.network_monitor', 'Netzwerk Traffic')}", NetworkMonitorWidget),
            (f"⚙️ {self.tr('widgets.gpu_monitor', 'GPU Monitor')}", GPUMonitorWidget),
            (f"⚙️ {self.tr('widgets.temp_monitor', 'Temperatur')}", TempMonitorWidget),
            (f"⚙️ {self.tr('widgets.disk_io_monitor', 'Datenträger I/O')}", DiskIOMonitorWidget),
            
            # File Manager
            (f"📁 {self.tr('widgets.directory_browser', 'Dateiverwaltung')}", DirectoryBrowserWidget),
            (f"📁 {self.tr('widgets.quick_access', 'Schnellzugriff')}", QuickAccessWidget),
            (f"📁 {self.tr('widgets.file_stats', 'Statistik')}", FileStatsWidget),
            (f"📁 {self.tr('widgets.recent_files', 'Zuletzt verwendet')}", RecentFilesWidget),
            
            # Network Diagnostics
            (f"🌐 {self.tr('widgets.ping', 'Ping')}", PingWidget),
            (f"🌐 {self.tr('widgets.connection_status', 'Verbindungsstatus')}", ConnectionStatusWidget),
            (f"🌐 {self.tr('widgets.speed_test', 'Speed Test')}", SpeedTestWidget),
            (f"🌐 {self.tr('widgets.active_connections', 'Aktive Verbindungen')}", ActiveConnectionsWidget),
            (f"🌐 {self.tr('widgets.network_path', 'Netzwerkpfad')}", NetworkPathWidget),
        ]
        
        for name, cls in items:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, cls)
            self.list_widget.addItem(item)
            
        self.list_widget.setCurrentRow(0)

    def _on_selection_changed(self, row):
        item = self.list_widget.item(row)
        self.current_widget_class = item.data(Qt.UserRole)
        
        # Get allowed sizes for this widget
        widget_name = self.current_widget_class.__name__
        allowed_sizes = self.WIDGET_SIZES.get(widget_name, [(1, 1), (2, 1), (2, 2)])  # Default
        
        # Rebuild size buttons
        self._rebuild_size_buttons(allowed_sizes)
        
        # Select first available size
        if allowed_sizes:
            self._update_preview(allowed_sizes[0][0], allowed_sizes[0][1])
    
    def _rebuild_size_buttons(self, allowed_sizes):
        """Rebuild size buttons based on allowed sizes for current widget."""
        # Clear existing buttons
        for btn in self.size_buttons:
            btn.deleteLater()
        self.size_buttons.clear()
        
        # Size labels
        size_labels = {
            (1, 1): self.tr("dialogs.widget_selector.sizes.compact", "Kompakt"), 
            (2, 1): self.tr("dialogs.widget_selector.sizes.wide", "Breit"), 
            (3, 1): self.tr("dialogs.widget_selector.sizes.extra_wide", "Extra Breit"), 
            (4, 1): self.tr("dialogs.widget_selector.sizes.full_width", "Volle Breite"),
            (1, 2): self.tr("dialogs.widget_selector.sizes.tall", "Hoch"), 
            (2, 2): self.tr("dialogs.widget_selector.sizes.large", "Groß"), 
            (3, 2): self.tr("dialogs.widget_selector.sizes.extra_large", "Extra Groß"), 
            (4, 2): self.tr("dialogs.widget_selector.sizes.maximum", "Maximum")
        }
        
        # Create button for each allowed size
        for w, h in allowed_sizes:
            label = size_labels.get((w, h), f"{w}x{h}")
            btn = QPushButton(f"{label} ({w}x{h})")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, width=w, height=h: self._update_preview(width, height))
            self.size_buttons_layout.addWidget(btn)
            self.size_buttons.append(btn)
        
        # Check first button
        if self.size_buttons:
            self.size_buttons[0].setChecked(True)

    def _update_preview(self, w, h):
        """Render a full snapshot of the selected widget for preview.
        The widget is instantiated at its actual size, rendered to a QPixmap,
        then scaled to fit the preview container while preserving visual fidelity.
        """
        self.current_span = (w, h)

        # Update button states
        for btn in self.size_buttons:
            text = btn.text()
            btn.setChecked(f"({w}x{h})" in text)

        # Clear previous preview widgets
        while self.preview_layout.count():
            child = self.preview_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.current_widget_class:
            return

        try:
            # Instantiate the widget with the requested span
            # Parent it to self to avoid top-level window flickering
            # But keep it hidden/off-screen initially
            widget = self.current_widget_class()
            widget.setParent(self) 
            
            # CRITICAL: Rebuild widget for the requested span if it supports it
            if hasattr(widget, 'rebuild_for_span'):
                widget.rebuild_for_span(w, h)
            else:
                # Fallback for widgets that don't support rebuild
                widget.span_w = w
                widget.span_h = h
                if hasattr(widget, '_update_size'):
                    widget._update_size()

            # Determine the widget's real size (base unit 160px)
            base_size = 160
            real_w = base_size * w
            real_h = base_size * h
            widget.setFixedSize(real_w, real_h)
            
            # Move off-screen to avoid visual flicker
            widget.move(-10000, -10000)

            # Ensure the widget is polished and laid out
            widget.show()
            widget.ensurePolished()
            
            # Force layout update - multiple passes for complex widgets
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()
            QApplication.processEvents()  # Second pass for nested layouts

            # Render to pixmap
            pixmap = widget.grab()
            
            # Cleanup
            widget.hide()
            widget.deleteLater()

            # Scale pixmap to fit preview area (max 380x280)
            max_w, max_h = 380, 280
            scale = min(max_w / real_w, max_h / real_h, 1.0)
            preview_pixmap = pixmap.scaled(int(real_w * scale), int(real_h * scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Display pixmap in a QLabel
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            preview_label.setPixmap(preview_pixmap)
            self.preview_layout.addWidget(preview_label)

            # Update preview description
            scale_text = self.tr("dialogs.widget_selector.scale", "Skalierung")
            preview_text = self.tr("dialogs.widget_selector.preview", "Vorschau")
            self.preview_label.setText(f"{preview_text} ({w}x{h} • ~{int(scale*100)}% {scale_text})")
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            error_title = self.tr("dialogs.widget_selector.error", "Vorschau-Fehler")
            err_label = QLabel(f"❌ {error_title}:\n{str(e)}\n\nDetails:\n{tb[:200]}")
            err_label.setAlignment(Qt.AlignCenter)
            err_label.setStyleSheet("color: #ff3b30; font-size: 10px; font-family: 'Consolas';")
            err_label.setWordWrap(True)
            self.preview_layout.addWidget(err_label)
            self.preview_label.setText(self.tr("dialogs.widget_selector.preview", "Vorschau"))
            print(f"Preview Error:\n{tb}")

    def _add_widget(self):
        if self.current_widget_class:
            self.widget_selected.emit(self.current_widget_class, self.current_span[0], self.current_span[1])
            self.accept()
