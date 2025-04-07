from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout

from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.widgets.text_based import StyledTextEdit

if TYPE_CHECKING:
    from battle_map_tv.window_image import ImageWindow


class InitiativeControls(QVBoxLayout):
    def __init__(self, image_window: "ImageWindow"):
        super().__init__()
        self.image_window = image_window

        self.setSpacing(20)
        self.addWidget(InitiativeTextArea(image_window))
        self.addLayout(InitiativeButtons(image_window))


class InitiativeTextArea(StyledTextEdit):
    def __init__(self, image_window: "ImageWindow"):
        super().__init__()
        self.image_window = image_window
        self.setPlaceholderText("Display initiative order")
        self.on_text_changed(self.callback)

    def callback(self):
        text = self.toPlainText().strip()
        self.image_window.add_initiative(text)


class InitiativeButtons(HorizontalLayout):
    def __init__(self, image_window: "ImageWindow"):
        super().__init__()
        self.add_button("+", lambda: image_window.initiative_change_font_size(by=2))
        self.add_button("-", lambda: image_window.initiative_change_font_size(by=-2))
        self.add_button("move", image_window.initiative_move)
