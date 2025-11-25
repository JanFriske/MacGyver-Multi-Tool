import platform
import psutil
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QPushButton, QHBoxLayout
from PySide6.QtCore import QTimer, Qt


class SystemInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_timer()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("System Information")
        header.setObjectName("h1")
        layout.addWidget(header)

        # Info Grid
        info_frame = QFrame()
        info_frame.setObjectName("card")
        grid = QGridLayout(info_frame)
        grid.setSpacing(15)

        # Static Info
        grid.addWidget(QLabel("Betriebssystem:"), 0, 0)
        grid.addWidget(QLabel(f"{platform.system()} {platform.release()}"), 0, 1)

        grid.addWidget(QLabel("Prozessor:"), 1, 0)
        grid.addWidget(QLabel(platform.processor()), 1, 1)

        grid.addWidget(QLabel("Maschine:"), 2, 0)
        grid.addWidget(QLabel(platform.machine()), 2, 1)

        layout.addWidget(info_frame)

        # Dynamic Info (CPU/RAM)
        stats_frame = QFrame()
        stats_frame.setObjectName("card")
        stats_layout = QVBoxLayout(stats_frame)
        
        self.cpu_label = QLabel("CPU Auslastung: ...")
        self.ram_label = QLabel("RAM Auslastung: ...")
        
        stats_layout.addWidget(self.cpu_label)
        stats_layout.addWidget(self.ram_label)

        layout.addWidget(stats_frame)

        # Button Row for Testing
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_refresh = QPushButton("Aktualisieren")
        self.btn_refresh.clicked.connect(self.update_stats)
        
        self.btn_action = QPushButton("Aktion")
        self.btn_action.setProperty("class", "primary") # For Blue Styling
        
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_action)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)


    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000) # Update every 2 seconds
        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_label.setText(f"CPU Auslastung: {cpu}%")
        self.ram_label.setText(f"RAM Auslastung: {ram}%")
