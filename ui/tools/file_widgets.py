from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                                QTreeWidget, QTreeWidgetItem, QScrollArea, QLineEdit, QSplitter)
from PySide6.QtCore import Qt, QTimer, Signal, QDir
from PySide6.QtGui import QIcon
from pathlib import Path
import os
from datetime import datetime

from ui.components.macgyver_widget import MacGyverWidget
from ui.components.premium_table import PremiumTableWidget
from ui.components.circular_gauge import CircularGauge


class DirectoryBrowserWidget(MacGyverWidget):
    """2x2 Directory Browser with tree and file list."""
    
    file_selected = Signal(str)
    
    def __init__(self):
        super().__init__(self._tr("widgets.directory_browser_title", "Dateiverwaltung"), size_span=(2, 2))
        self.current_path = Path.home()
        self._init_ui()
        self._load_directory(self.current_path)
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        self._init_ui()
        self._load_directory(self.current_path)

    def _init_ui(self):
        # Clear existing
        if self.content_area.count():
            while self.content_area.count():
                item = self.content_area.takeAt(0)
                if item.widget(): item.widget().deleteLater()

        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Path bar
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(str(self.current_path))
        self.path_input.returnPressed.connect(self._navigate_to_path)
        path_layout.addWidget(QLabel("📁"))
        path_layout.addWidget(self.path_input)
        
        up_btn = QPushButton(self._tr("file_manager.up_button", "⬆️ Up"))
        up_btn.clicked.connect(self._navigate_up)
        path_layout.addWidget(up_btn)
        layout.addLayout(path_layout)
        
        # Split view: Tree | File List
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Directory tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Ordner")
        self.tree.itemClicked.connect(self._tree_item_clicked)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: rgba(30, 30, 30, 0.5);
                border: none;
                border-radius: 8px;
                color: #e0e0e0;
            }
            QTreeWidget::item:selected {
                background-color: rgba(0, 122, 255, 0.3);
            }
        """)
        splitter.addWidget(self.tree)
        
        # Right: File table
        self.table = PremiumTableWidget([self._tr("file_manager.headers.name", "Name"), self._tr("file_manager.headers.size", "Size"), self._tr("file_manager.headers.modified", "Modified")])
        self.table.row_double_clicked.connect(self._file_double_clicked)
        splitter.addWidget(self.table)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)
        
        self.add_bubble(container)
    
    def _load_directory(self, path):
        """Load directory tree and file list."""
        try:
            self.current_path = Path(path)
            if hasattr(self, 'path_input'):
                self.path_input.setText(str(self.current_path))
            
            # Update tree
            if hasattr(self, 'tree'):
                self.tree.clear()
                self._populate_tree(self.tree.invisibleRootItem(), self.current_path.parent)
            
            # Update file list
            if hasattr(self, 'table'):
                self._load_files()
        except Exception as e:
            print(f"Error loading directory: {e}")
    
    def _populate_tree(self, parent_item, path):
        """Populate tree with subdirectories."""
        try:
            path = Path(path)
            for item in sorted(path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    tree_item = QTreeWidgetItem(parent_item, [item.name])
                    tree_item.setData(0, Qt.UserRole, str(item))
        except:
            pass
    
    def _load_files(self):
        """Load files in current directory into table."""
        self.table.clear_rows()
        try:
            for item in sorted(self.current_path.iterdir()):
                name = item.name
                if item.is_file():
                    size = self._format_size(item.stat().st_size)
                    modified = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    self.table.add_row([name, size, modified])
                elif item.is_dir():
                    self.table.add_row([f"📁 {name}", "—", "—"])
        except Exception as e:
            print(f"Error loading files: {e}")
    
    def _format_size(self, size):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def _tree_item_clicked(self, item, column):
        """Handle tree item click."""
        path = item.data(0, Qt.UserRole)
        if path:
            self._load_directory(path)
    
    def _file_double_clicked(self, row):
        """Handle file double-click."""
        row_data = self.table.get_row_data(row)
        name = row_data[0].replace("📁 ", "")
        file_path = self.current_path / name
        
        if file_path.is_dir():
            self._load_directory(file_path)
        else:
            os.startfile(str(file_path))  # Windows
            self.file_selected.emit(str(file_path))
    
    def _navigate_up(self):
        """Navigate to parent directory."""
        parent = self.current_path.parent
        if parent != self.current_path:
            self._load_directory(parent)
    
    def _navigate_to_path(self):
        """Navigate to path from input."""
        path = Path(self.path_input.text())
        if path.exists() and path.is_dir():
            self._load_directory(path)


class QuickAccessWidget(MacGyverWidget):
    """1x1 Quick access to favorite folders."""
    
    folder_clicked = Signal(str)
    
    def __init__(self):
        super().__init__(self._tr("widgets.quick_access_title", "Schnellzugriff"), size_span=(1, 1))
        self._init_ui()
    
    def rebuild_for_span(self, w, h):
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        self._init_ui()

    def _init_ui(self):
        # Clear existing
        if self.content_area.count():
            while self.content_area.count():
                item = self.content_area.takeAt(0)
                if item.widget(): item.widget().deleteLater()

        container = QWidget()
        
        # Responsive layout based on widget size
        if self.span_w == 1 and self.span_h == 1:
            # 1x1: Single column, compact buttons
            layout = QVBoxLayout(container)
            button_height = 28  # Reduced from 32px
            max_buttons = 4
            layout.setSpacing(4) # Tighter spacing for 1x1
        else:  # 2x1 or larger
            # 2x1: Two columns for more buttons
            layout = QGridLayout(container)
            button_height = 32
            max_buttons = 8
            layout.setSpacing(8)
        
        # System folders
        folders = [
            ("🖥️ Desktop", Path.home() / "Desktop"),
            ("📄 Documents", Path.home() / "Documents"),
            ("⬇️ Downloads", Path.home() / "Downloads"),
            ("🖼️ Pictures", Path.home() / "Pictures"),
            ("🎵 Music", Path.home() / "Music"),
            ("🎬 Videos", Path.home() / "Videos"),
            ("📁 Home", Path.home()),
            ("💼 Desktop", Path.home() / "Desktop"),
        ]
        
        for idx, (icon_name, path) in enumerate(folders[:max_buttons]):
            btn = QPushButton(icon_name)
            btn.setFixedHeight(button_height)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 50, 50, 0.6);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 6px;
                    color: #e0e0e0;
                    text-align: left;
                    padding-left: 10px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: rgba(70, 70, 70, 0.8);
                    border-color: rgba(0, 122, 255, 0.5);
                }
                QPushButton:pressed {
                    background-color: rgba(0, 122, 255, 0.3);
                }
            """)
            btn.clicked.connect(lambda checked, p=path: self.folder_clicked.emit(str(p)))
            
            if self.span_w == 1 and self.span_h == 1:
                # Single column
                layout.addWidget(btn)
            else:
                # Grid layout: 2 columns
                row = idx // 2
                col = idx % 2
                layout.addWidget(btn, row, col)
        
        if self.span_w == 1 and self.span_h == 1:
            layout.addStretch()
        
        self.add_bubble(container)


class FileStatsWidget(MacGyverWidget):
    """1x1 Current directory statistics."""
    
    def __init__(self):
        super().__init__(self._tr("widgets.file_stats_title", "Statistik"), size_span=(1, 1))
        self.current_path = Path.home()
        self._init_ui()
        self._update_stats()
    
    def rebuild_for_span(self, w, h):
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        self._init_ui()
        self._update_stats()

    def _init_ui(self):
        # Clear existing
        if self.content_area.count():
            while self.content_area.count():
                item = self.content_area.takeAt(0)
                if item.widget(): item.widget().deleteLater()

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        
        # Responsive sizing based on widget size
        if self.span_w == 1 and self.span_h == 1:
            gauge_size = 60  # Reduced from 80px
            label_size = 16
            size_label_size = 13
        else:  # 2x1 or larger
            gauge_size = 85
            label_size = 18
            size_label_size = 14
        
        self.file_count_label = QLabel("0 Dateien")
        self.file_count_label.setAlignment(Qt.AlignCenter)
        self.file_count_label.setStyleSheet(f"font-size: {label_size}px; font-weight: bold; color: #007aff;")
        layout.addWidget(self.file_count_label)
        
        self.size_label = QLabel("0 MB")
        self.size_label.setAlignment(Qt.AlignCenter)
        self.size_label.setStyleSheet(f"font-size: {size_label_size}px; color: #aaa;")
        layout.addWidget(self.size_label)
        
        # Space gauge
        self.space_gauge = CircularGauge(self._tr("widgets.file_stats_storage", "Speicher"), unit="%", size=gauge_size)
        layout.addWidget(self.space_gauge, alignment=Qt.AlignCenter)
        
        self.add_bubble(container)
    
    def set_path(self, path):
        """Update stats for a specific path."""
        self.current_path = Path(path)
        self._update_stats()
    
    def _update_stats(self):
        """Update statistics display."""
        try:
            files = list(self.current_path.glob("*"))
            file_count = len([f for f in files if f.is_file()])
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            
            if hasattr(self, 'file_count_label'):
                self.file_count_label.setText(f"{file_count} Dateien")
            if hasattr(self, 'size_label'):
                self.size_label.setText(self._format_size(total_size))
            
            # Disk space usage
            import shutil
            usage = shutil.disk_usage(self.current_path)
            percent = (usage.used / usage.total) * 100
            if hasattr(self, 'space_gauge'):
                self.space_gauge.set_value(percent)
        except Exception as e:
            print(f"Error updating stats: {e}")
    
    def _format_size(self, size):
        """Format file size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


class RecentFilesWidget(MacGyverWidget):
    """2x1 Recently accessed files."""
    
    file_clicked = Signal(str)
    
    def __init__(self):
        super().__init__(self._tr("widgets.recent_files_title", "Zuletzt verwendet"), size_span=(2, 1))
        self.recent_files = []
        self._init_ui()
        self._load_recent_files()
    
    def rebuild_for_span(self, w, h):
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        self._init_ui()
        self._display_files()

    def _init_ui(self):
        # Clear existing
        if self.content_area.count():
            while self.content_area.count():
                item = self.content_area.takeAt(0)
                if item.widget(): item.widget().deleteLater()

        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.layout.setSpacing(10)
        
        # Scrollable area for file cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        self.files_container = QWidget()
        self.files_layout = QHBoxLayout(self.files_container)
        self.files_layout.setSpacing(8)
        scroll.setWidget(self.files_container)
        
        self.layout.addWidget(scroll)
        self.add_bubble(container)
    
    def _load_recent_files(self):
        """Load recently accessed files (stub - would use system API)."""
        # For now, show recent files from Downloads
        try:
            downloads = Path.home() / "Downloads"
            if downloads.exists():
                files = sorted(downloads.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]
                self.recent_files = [f for f in files if f.is_file()]
                self._display_files()
        except:
            pass
    
    def _display_files(self):
        """Display file cards."""
        if not hasattr(self, 'files_layout'): return

        # Clear existing
        while self.files_layout.count():
            child = self.files_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add file cards
        for file_path in self.recent_files:
            card = self._create_file_card(file_path)
            self.files_layout.addWidget(card)
        
        self.files_layout.addStretch()
    
    def _create_file_card(self, file_path):
        """Create a file card widget."""
        card = QPushButton()
        card.setFixedSize(120, 80)
        
        # Get file info
        name = file_path.name
        if len(name) > 15:
            name = name[:12] + "..."
        timestamp = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%H:%M")
        
        card.setText(f"📄\n{name}\n{timestamp}")
        card.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #e0e0e0;
                font-size: 11px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: rgba(70, 70, 70, 0.8);
                border-color: rgba(0, 122, 255, 0.5);
            }
        """)
        card.clicked.connect(lambda: self.file_clicked.emit(str(file_path)))
        
        return card
