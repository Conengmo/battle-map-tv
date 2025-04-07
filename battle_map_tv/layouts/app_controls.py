from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.utils import get_current_application, get_image_window
from battle_map_tv.widgets.buttons import StyledButton


class AppControlsLayout(HorizontalLayout):
    """A horizontal layout with buttons to control the application."""

    def __init__(self):
        super().__init__()
        image_window = get_image_window()
        app = get_current_application()

        button = StyledButton("Fullscreen")
        button.clicked.connect(image_window.toggle_fullscreen)
        self.addWidget(button)

        button = StyledButton("Exit")
        button.clicked.connect(app.quit)
        self.addWidget(button)
