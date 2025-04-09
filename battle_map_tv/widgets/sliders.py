from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider


class StyledSlider(QSlider):
    def __init__(self, lower: int, upper: int, default: int, *args, **kwargs):
        super().__init__(Qt.Horizontal, *args, **kwargs)  # type: ignore[attr-defined]
        self.setMinimum(lower)
        self.setMaximum(upper)
        self.setValue(default)
        self.setStyleSheet(
            """
            QSlider {
                height: 40px;
            }
            QSlider::groove:horizontal {
                height: 10px;
                background: #404040;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background: #717173;
                border: 1px solid #3E3E40;
                width: 20px;
                margin: -15px 0;
                border-radius: 6px;
            }
        """
        )
