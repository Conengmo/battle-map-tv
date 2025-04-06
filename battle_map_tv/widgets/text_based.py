from typing import Callable

from PySide6.QtCore import QTimer
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

    def connect_text_changed_callback_with_timer(self, callback: Callable):
        typing_timer = QTimer()
        typing_timer.setSingleShot(True)
        typing_timer.timeout.connect(callback)

        def reset_typing_timer():
            typing_timer.start(700)

        self.textChanged.connect(reset_typing_timer)
