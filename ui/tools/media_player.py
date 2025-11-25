from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QStyle, QFileDialog
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QTime

class MediaPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()
        self._init_player()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Video Widget
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Controls Container
        self.controls_layout = QHBoxLayout()
        self.controls_layout.setContentsMargins(10, 0, 10, 10)

        # Play/Pause Button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.toggle_playback)
        self.controls_layout.addWidget(self.play_button)

        # Stop Button
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.clicked.connect(self.stop_playback)
        self.controls_layout.addWidget(self.stop_button)

        # Seek Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.controls_layout.addWidget(self.slider)

        # Time Label
        self.time_label = QLabel("00:00 / 00:00")
        self.controls_layout.addWidget(self.time_label)

        # Open Button
        self.open_button = QPushButton(self.tr("media.open_button", "Öffnen"))
        self.open_button.clicked.connect(self.open_file)
        self.controls_layout.addWidget(self.open_button)

        self.layout.addLayout(self.controls_layout)

    def _init_player(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # Connect Signals
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.playbackStateChanged.connect(self.media_state_changed)
        self.media_player.errorOccurred.connect(self.handle_errors)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Video files (*.mp4 *.avi *.mkv *.mov *.wmv)", "Audio files (*.mp3 *.wav *.ogg)", "All files (*)"])
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            if files:
                self.media_player.setSource(QUrl.fromLocalFile(files[0]))
                self.play_button.setEnabled(True)
                self.media_player.play()

    def toggle_playback(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop_playback(self):
        self.media_player.stop()

    def media_state_changed(self, state):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
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

    def handle_errors(self):
        self.play_button.setEnabled(False)
        self.time_label.setText(f"Error: {self.media_player.errorString()}")
