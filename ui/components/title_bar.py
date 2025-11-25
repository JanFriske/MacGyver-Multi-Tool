from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, QSize, QEvent

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(30)
        self._init_ui()
        self.start_pos = None

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)

        # Traffic Light Buttons
        self.btn_close = self._create_traffic_light("close", "#FF5F56", "#E0443E", "×")
        self.btn_minimize = self._create_traffic_light("minimize", "#FFBD2E", "#DEA123", "−")
        self.btn_maximize = self._create_traffic_light("maximize", "#27C93F", "#1AAB29", "+")

        layout.addWidget(self.btn_close)
        layout.addWidget(self.btn_minimize)
        layout.addWidget(self.btn_maximize)

        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Title
        # Version can be passed or hardcoded for now
        version = "v1.0" 
        self.title_label = QLabel(f"MacGyver Multi-Tool {version}")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-family: 'Segoe UI', sans-serif; font-size: 13px;")
        layout.addWidget(self.title_label)

        # App Icon (Right of Title)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(16, 16)
        self.icon_label.setScaledContents(True)
        # Load icon
        from PySide6.QtGui import QPixmap
        import os
        icon_path = os.path.join("assets", "icons", "mgmt.ico")
        if os.path.exists(icon_path):
             self.icon_label.setPixmap(QPixmap(icon_path))
        layout.addWidget(self.icon_label)
        
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.setLayout(layout)

        # Connect buttons
        self.btn_close.clicked.connect(self.parent_window.close)
        self.btn_minimize.clicked.connect(self.parent_window.showMinimized)
        self.btn_maximize.clicked.connect(self._toggle_maximize)

    def _create_traffic_light(self, name, color, hover_color, symbol):
        btn = TrafficLightButton(name, symbol, color, hover_color)
        btn.setFixedSize(12, 12)
        return btn

    def _toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()

    # Window Dragging Logic
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.start_pos:
            self.parent_window.move(event.globalPosition().toPoint() - self.start_pos)
            event.accept()

class TrafficLightButton(QPushButton):
    def __init__(self, name, symbol, color, hover_color):
        super().__init__()
        self.name = f"btn_{name}"
        self.setObjectName(self.name)
        self.symbol = symbol
        # Colors are now handled by QSS
        self.setText("")

    def enterEvent(self, event):
        self.setText(self.symbol)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setText("")
        super().leaveEvent(event)
