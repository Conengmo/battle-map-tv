from PySide6.QtWidgets import QGridLayout


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
