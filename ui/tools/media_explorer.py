from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QHeaderView
from PySide6.QtCore import Signal, QDir, QModelIndex

class MediaExplorerWidget(QWidget):
    file_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setNameFilters(["*.mp3", "*.wav", "*.ogg", "*.mp4", "*.avi", "*.mkv", "*.mov", "*.wmv", "*.flac", "*.m4a"])
        self.model.setNameFilterDisables(False)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath())) # Start in Home directory
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        
        # Hide size, type, date columns for cleaner look, keep only Name
        self.tree.setColumnWidth(0, 250)
        self.tree.hideColumn(1) # Size
        self.tree.hideColumn(2) # Type
        self.tree.hideColumn(3) # Date

        self.tree.doubleClicked.connect(self._on_double_click)
        
        self.layout.addWidget(self.tree)

    def _on_double_click(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        if self.model.isDir(index):
            return
        self.file_selected.emit(file_path)
