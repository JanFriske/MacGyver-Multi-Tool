from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QComboBox, QFrame
)
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush
import random

class Visualizer(QWidget):
    def __init__(self, bands=10):
        super().__init__()
        self.bands = bands
        self.levels = [0.0] * bands
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_levels)
        self.timer.start(50) # 20 FPS
        self.setMinimumHeight(100)

    def update_levels(self):
        # Simulate audio data (since we can't easily get real FFT from QMediaPlayer in Python)
        for i in range(self.bands):
            target = random.random()
            # Smooth transition
            self.levels[i] = self.levels[i] * 0.6 + target * 0.4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        bar_w = w / self.bands
        
        # Gradient for bars
        gradient = QLinearGradient(0, h, 0, 0)
        gradient.setColorAt(0.0, QColor("#007aff"))
        gradient.setColorAt(1.0, QColor("#00c6ff"))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)

        for i in range(self.bands):
            bar_h = self.levels[i] * h
            x = i * bar_w + 2
            y = h - bar_h
            
            # Draw bar
            painter.drawRoundedRect(QRectF(x, y, bar_w - 4, bar_h), 4, 4)

class EqualizerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Header / Presets
        header_layout = QHBoxLayout()
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            self._tr("media.equalizer_presets.flat", "Flat"),
            self._tr("media.equalizer_presets.rock", "Rock"),
            self._tr("media.equalizer_presets.pop", "Pop"),
            self._tr("media.equalizer_presets.jazz", "Jazz"),
            self._tr("media.equalizer_presets.classical", "Classical"),
            self._tr("media.equalizer_presets.bass_boost", "Bass Boost")
        ])
        self.preset_combo.currentTextChanged.connect(self.apply_preset)
        header_layout.addWidget(QLabel(self._tr("media.equalizer_preset_label", "Preset:")))
        header_layout.addWidget(self.preset_combo)
        header_layout.addStretch()
        self.layout.addLayout(header_layout)

        # Visualizer
        self.visualizer = Visualizer(bands=10)
        self.layout.addWidget(self.visualizer)

        # Sliders
        sliders_layout = QHBoxLayout()
        self.sliders = []
        frequencies = ["32", "64", "125", "250", "500", "1k", "2k", "4k", "8k", "16k"]
        
        for freq in frequencies:
            v_layout = QVBoxLayout()
            slider = QSlider(Qt.Vertical)
            slider.setRange(-12, 12)
            slider.setValue(0)
            slider.setTickPosition(QSlider.TicksBothSides)
            self.sliders.append(slider)
            
            v_layout.addWidget(slider)
            label = QLabel(freq)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 10px; color: #888;")
            v_layout.addWidget(label)
            
            sliders_layout.addLayout(v_layout)
            
        self.layout.addLayout(sliders_layout)

    def apply_preset(self, preset_name):
        # Dummy preset logic
        values = [0] * 10
        if preset_name == "Rock": values = [4, 3, 2, 0, -1, -1, 0, 2, 3, 4]
        elif preset_name == "Pop": values = [-1, 1, 3, 4, 4, 3, 1, -1, -1, -1]
        elif preset_name == "Bass Boost": values = [6, 5, 4, 2, 0, 0, 0, 0, 0, 0]
        
        for slider, val in zip(self.sliders, values):
            slider.setValue(val)
