from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtMultimediaWidgets import QVideoWidget

class VideoScreenWidget(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)
        
        # Set this widget as the video output for the player
        self.media_player.setVideoOutput(self.video_widget)
