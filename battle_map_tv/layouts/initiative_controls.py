from PySide6.QtWidgets import QVBoxLayout

from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.utils import get_image_window
from battle_map_tv.widgets.text_based import StyledTextEdit


class InitiativeControls(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(20)
        self.addWidget(InitiativeTextArea())
        self.addLayout(InitiativeButtons())


class InitiativeTextArea(StyledTextEdit):
    def __init__(self):
        super().__init__()
        self.image_window = get_image_window()
        self.setPlaceholderText("Display initiative order")
        self.on_text_changed(self.callback)

    def callback(self):
        text = self.toPlainText().strip()
        self.image_window.add_initiative(text)


class InitiativeButtons(HorizontalLayout):
    def __init__(self):
        super().__init__()
        image_window = get_image_window()
        self.add_button("+", lambda: image_window.initiative_change_font_size(by=2))
        self.add_button("-", lambda: image_window.initiative_change_font_size(by=-2))
        self.add_button("move", image_window.initiative_move)
