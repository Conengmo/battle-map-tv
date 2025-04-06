from typing import Callable

from battle_map_tv.layouts.base import FixedRowGridLayout
from battle_map_tv.widgets.buttons import ColorSelectionButton


class ColorSelectionWindow(FixedRowGridLayout):
    def __init__(self, callback: Callable):
        super().__init__(rows=2)
        self.colors = [
            "#ff3d00",
            "#48ABB4",
            "#009E00",
            "#9702A7",
            "#FFF800",
            "grey",
            "black",
            "white",
        ]
        self.buttons = []
        for color in self.colors:
            button = ColorSelectionButton(color=color)
            button.clicked.connect(self.create_color_selected_handler(color, callback))
            self.add_widget(button)
            self.buttons.append(button)
        self.selected_color: str
        self.buttons[-1].click()

    def create_color_selected_handler(self, color: str, callback: Callable):
        def handler():
            self.selected_color = color
            for button in self.buttons:
                if button.color == color:
                    button.setStyleSheet(button.selected_stylesheet)
                else:
                    button.setStyleSheet(button.default_stylesheet)
            callback(color)

        return handler
