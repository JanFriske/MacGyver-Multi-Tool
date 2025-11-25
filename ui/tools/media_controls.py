from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QStyle, QFileDialog, QFrame
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import Qt, QUrl, QTime, QTimer, QSize

class MarqueeLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.px = 0
        self.py = 0
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.scroll)
        self.scroll_timer.start(30)
        self.setText(text)

    def scroll(self):
        if self.text():
            self.px -= 1
            if self.px < -self.fontMetrics().horizontalAdvance(self.text()):
                self.px = self.width()
            self.update()

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter
        painter = QPainter(self)
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        if text_width > self.width():
            painter.drawText(self.px, self.py + self.fontMetrics().ascent(), self.text())
        else:
            super().paintEvent(event)

class MediaControlWidget(QWidget):
    def __init__(self, media_player, audio_output):
        super().__init__()
        self.media_player = media_player
        self.audio_output = audio_output
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Marquee Display
        self.info_display = MarqueeLabel("Keine Medienwiedergabe...")
        self.info_display.setStyleSheet("font-size: 14px; font-weight: bold; color: #007aff; margin-bottom: 5px;")
        self.info_display.setFixedHeight(30)
        self.layout.addWidget(self.info_display)

        # Seek Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.layout.addWidget(self.slider)

        # Time Label
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        # Controls Row 1: Transport
        self.controls_layout = QHBoxLayout()
        
        self.btn_first = QPushButton("⏮") # First
        self.btn_prev = QPushButton("⏪") # Prev
        self.btn_play = QPushButton()
        self.btn_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btn_stop = QPushButton()
        self.btn_stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.btn_next = QPushButton("⏩") # Next
        self.btn_last = QPushButton("⏭") # Last

        self.controls_layout.addWidget(self.btn_first)
        self.controls_layout.addWidget(self.btn_prev)
        self.controls_layout.addWidget(self.btn_play)
        self.controls_layout.addWidget(self.btn_stop)
        self.controls_layout.addWidget(self.btn_next)
        self.controls_layout.addWidget(self.btn_last)
        
        self.layout.addLayout(self.controls_layout)

        # Controls Row 2: Audio & File
        self.audio_layout = QHBoxLayout()
        
        self.btn_mute = QPushButton("🔊")
        self.btn_mute.setCheckable(True)
        self.btn_mute.clicked.connect(self.toggle_mute)
        self.audio_layout.addWidget(self.btn_mute)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.audio_output.setVolume(0.7)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.audio_layout.addWidget(self.volume_slider)

        self.btn_open = QPushButton("⏏ Öffnen")
        self.btn_open.clicked.connect(self.open_file)
        self.audio_layout.addWidget(self.btn_open)

        self.layout.addLayout(self.audio_layout)

        # Connect Buttons
        self.btn_play.clicked.connect(self.toggle_playback)
        self.btn_stop.clicked.connect(self.stop_playback)
        # Placeholder connections for Next/Prev/First/Last (logic depends on playlist)
        self.btn_first.clicked.connect(lambda: self.media_player.setPosition(0))
        self.btn_prev.clicked.connect(lambda: self.media_player.setPosition(max(0, self.media_player.position() - 5000))) # -5 sec
        self.btn_next.clicked.connect(lambda: self.media_player.setPosition(min(self.media_player.duration(), self.media_player.position() + 5000))) # +5 sec
        self.btn_last.clicked.connect(lambda: self.media_player.setPosition(self.media_player.duration()))

    def _connect_signals(self):
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.playbackStateChanged.connect(self.media_state_changed)
        self.media_player.errorOccurred.connect(self.handle_errors)
        self.media_player.metaDataChanged.connect(self.update_metadata)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Media files (*.mp4 *.avi *.mkv *.mp3 *.wav *.ogg)", "All files (*)"])
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            if files:
                self.media_player.setSource(QUrl.fromLocalFile(files[0]))
                self.media_player.play()
                self.info_display.setText(files[0].split('/')[-1]) # Simple filename as fallback

    def toggle_playback(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop_playback(self):
        self.media_player.stop()

    def media_state_changed(self, state):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.btn_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.btn_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        if not self.slider.isSliderDown():
            self.slider.setValue(position)
        self.update_duration_info(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_duration_info(self, current_info):
        duration = self.media_player.duration()
        if duration >= 0:
            t_str = QTime(0, 0, 0).addMSecs(current_info).toString("mm:ss")
            d_str = QTime(0, 0, 0).addMSecs(duration).toString("mm:ss")
            self.time_label.setText(f"{t_str} / {d_str}")

    def set_volume(self, volume):
        self.audio_output.setVolume(volume / 100)

    def toggle_mute(self):
        is_muted = self.audio_output.isMuted()
        self.audio_output.setMuted(not is_muted)
        self.btn_mute.setText("🔇" if not is_muted else "🔊")

    def handle_errors(self):
        self.btn_play.setEnabled(False)
        self.info_display.setText(f"Error: {self.media_player.errorString()}")

    def update_metadata(self):
        # Try to get title/artist from metadata
        # Note: PySide6 metadata handling can be tricky, fallback to filename is already in open_file
        pass
