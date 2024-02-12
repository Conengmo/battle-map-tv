from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from battle_map_tv.image import Image


class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            background-color: #262626;
            color: #FFFFFF;
            font-family: Titillium;
            font-size: 18px;
        """
        )

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.image: Optional[Image] = None

    def make_fullscreen(self):
        screen = self.screen()
        screen_resolution = screen.size()
        self.setFixedSize(screen_resolution)
        self.showFullScreen()

    def add_image(self, image_path: str):
        self.image = Image(
            image_path=image_path,
            layout=self.layout,
            window_width_px=self.width(),
            window_height_px=self.height(),
        )
        self.layout.update()

    def remove_image(self):
        if self.image is not None:
            self.image.delete()
            self.image = None
