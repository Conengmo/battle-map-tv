from typing import Callable

from PySide6.QtWidgets import QGridLayout, QHBoxLayout

from battle_map_tv.widgets.buttons import StyledButton


class HorizontalLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(20)

    def add_button(self, text: str, callback: Callable, **kwargs):
        button = StyledButton(text, **kwargs)
        button.clicked.connect(callback)
        self.addWidget(button)


class FixedRowGridLayout(QGridLayout):
    def __init__(self, rows: int):
        super().__init__()
        self.rows = rows
        self._i = 0
        self._j = 0
        self.setHorizontalSpacing(8)
        self.setVerticalSpacing(5)

    def add_widget(self, widget):
        super().addWidget(widget, self._i, self._j)
        self._i += 1
        if self._i >= self.rows:
            self._i = 0
            self._j += 1
