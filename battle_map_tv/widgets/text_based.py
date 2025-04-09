from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QLineEdit, QTextEdit


class StyledLineEdit(QLineEdit):
    def __init__(
        self,
        max_length: int,
        width: int,
        placeholder: str = "",
        value: str = "",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.setMaxLength(max_length)
        self.setFixedWidth(width)
        if placeholder:
            self.setPlaceholderText(placeholder)
        if value:
            self.setText(value)
        self.setStyleSheet(
            """
            QLineEdit {
                background-color: #101010;
                color: #E5E5E5;
                padding: 9px 20px;
                border: 1px solid #3E3E40;
                border-radius: 6px;
            }
        """
        )


class StyledTextEdit(QTextEdit):
    text_changed_debounce_ms = 700
    textChangedDebounced = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            background-color: #101010;
            color: #E5E5E5;
            padding: 9px 20px;
            border: 1px solid #3E3E40;
            border-radius: 6px;
        """
        )
        self._typing_timer = QTimer()
        self._typing_timer.setSingleShot(True)
        self._typing_timer.timeout.connect(self.textChangedDebounced.emit)

        self.textChanged.connect(self._reset_typing_timer)

    def _reset_typing_timer(self):
        self._typing_timer.start(self.text_changed_debounce_ms)
