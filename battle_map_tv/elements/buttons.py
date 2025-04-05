from PySide6.QtWidgets import QPushButton


class StyledButton(QPushButton):
    def __init__(self, *args, checkable: bool = False, padding_factor: float = 1.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCheckable(checkable)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #101010;
                padding: {10 * padding_factor:.0f}px {20 * padding_factor:.0f}px;
                border: 2px solid #3E3E40;
                border-radius: 6px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: #202020;
            }}
            QPushButton:checked {{
                background-color: #808080;
            }}
            QPushButton:disabled {{
                color: #696969;
                border: 2px solid #2b2b2c;
            }}
        """
        )


class ColorSelectionButton(QPushButton):
    def __init__(self, color: str):
        super().__init__()
        self.color = color
        stylesheet_template = """
            background-color: {color};
            border: 2px solid {border_color};
            padding: 6px 0;
        """
        self.default_stylesheet = stylesheet_template.format(color=color, border_color="grey")
        self.selected_stylesheet = stylesheet_template.format(color=color, border_color="white")
        self.setStyleSheet(self.default_stylesheet)
