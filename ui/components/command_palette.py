from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, 
    QWidget, QLabel, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize, QEvent
from PySide6.QtGui import QColor, QAction, QKeyEvent

class CommandPalette(QDialog):
    """
    A macOS-style Command Palette (Spotlight/Alfred style) for quick actions.
    """
    action_triggered = Signal(object)  # Emits the triggered QAction or callable

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(600, 400)
        
        self._init_ui()
        self.actions_list = [] # List of (name, callback/action) tuples

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Main Container
        self.container = QWidget()
        self.container.setObjectName("CommandPaletteContainer")
        self.container.setStyleSheet("""
            #CommandPaletteContainer {
                background-color: rgba(30, 30, 30, 0.95);
                border: 1px solid #444;
                border-radius: 12px;
            }
        """)
        
        # Drop Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.container.setGraphicsEffect(shadow)
        
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type a command...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #444;
                color: #fff;
                font-size: 18px;
                padding: 15px;
                selection-background-color: #007aff;
            }
        """)
        self.search_input.textChanged.connect(self._filter_actions)
        self.container_layout.addWidget(self.search_input)
        
        # Results List
        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                color: #ddd;
                padding: 10px 15px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            QListWidget::item:selected {
                background-color: #007aff;
                color: white;
            }
        """)
        self.results_list.itemActivated.connect(self._execute_selected)
        self.container_layout.addWidget(self.results_list)
        
        self.layout.addWidget(self.container)
        
        # Event Filter for navigation
        self.search_input.installEventFilter(self)

    def set_actions(self, actions):
        """
        Sets the list of available actions.
        actions: list of tuples (display_name, callback_or_qaction)
        """
        self.actions_list = actions
        self._filter_actions("")

    def _filter_actions(self, text):
        self.results_list.clear()
        text = text.lower()
        
        for name, action in self.actions_list:
            if text in name.lower():
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, action)
                self.results_list.addItem(item)
        
        if self.results_list.count() > 0:
            self.results_list.setCurrentRow(0)

    def _execute_selected(self, item=None):
        if not item:
            item = self.results_list.currentItem()
        
        if item:
            action = item.data(Qt.UserRole)
            self.action_triggered.emit(action)
            self.accept()

    def eventFilter(self, obj, event):
        if obj == self.search_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Down:
                curr = self.results_list.currentRow()
                if curr < self.results_list.count() - 1:
                    self.results_list.setCurrentRow(curr + 1)
                return True
            elif event.key() == Qt.Key_Up:
                curr = self.results_list.currentRow()
                if curr > 0:
                    self.results_list.setCurrentRow(curr - 1)
                return True
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self._execute_selected()
                return True
            elif event.key() == Qt.Key_Escape:
                self.reject()
                return True
                
        return super().eventFilter(obj, event)

    def show_centered(self, parent_window):
        # Center on parent
        geo = parent_window.geometry()
        center = geo.center()
        self.move(center.x() - self.width() // 2, center.y() - self.height() // 4) # Slightly above center
        self.search_input.setFocus()
        self.search_input.clear()
        self.show()
