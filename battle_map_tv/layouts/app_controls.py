from typing import TYPE_CHECKING

from PySide6.QtWidgets import QApplication

from battle_map_tv.widgets.buttons import StyledButton
from battle_map_tv.layouts.base import HorizontalLayout

if TYPE_CHECKING:
    from battle_map_tv.window_image import ImageWindow


class AppControlsLayout(HorizontalLayout):
    """A horizontal layout with buttons to control the application."""

    def __init__(self, image_window: "ImageWindow", app: QApplication):
        super().__init__()
        button = StyledButton("Fullscreen")
        button.clicked.connect(image_window.toggle_fullscreen)
        self.addWidget(button)

        button = StyledButton("Exit")
        button.clicked.connect(app.quit)
        self.addWidget(button)
