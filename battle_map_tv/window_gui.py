from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from battle_map_tv.layouts.app_controls import AppControlsLayout
from battle_map_tv.layouts.area_of_effect_controls import AreaOfEffectControls
from battle_map_tv.layouts.grid_controls import GridControls
from battle_map_tv.layouts.image_controls import ImageButtonsLayout, ImageScaleSlidersLayout
from battle_map_tv.widgets import get_window_icon
from battle_map_tv.widgets.buttons import StyledButton
from battle_map_tv.widgets.text_based import StyledTextEdit
from battle_map_tv.window_image import ImageWindow


class GuiWindow(QWidget):
    def __init__(
        self,
        image_window: ImageWindow,
        app: QApplication,
        default_directory: Optional[str],
    ):
        super().__init__()
        self.image_window = image_window
        self.app = app

        self.setWindowTitle("Controls")
        self.setWindowIcon(get_window_icon())
        self.setStyleSheet(
            """
            background-color: #000000;
            color: #E5E5E5;
            font-size: 18px;
        """
        )

        self._superlayout = QHBoxLayout(self)
        self._superlayout.setAlignment(Qt.AlignVCenter)  # type: ignore[attr-defined]
        self._superlayout.setContentsMargins(60, 80, 80, 80)
        self._superlayout.setSpacing(50)

        self.add_column_initiative()

        self._layout = QVBoxLayout()
        self._superlayout.addLayout(self._layout)

        self._layout.addLayout(
            ImageButtonsLayout(image_window=image_window, default_directory=default_directory)
        )
        self._layout.addLayout(ImageScaleSlidersLayout(image_window=image_window))
        self._layout.addLayout(GridControls(image_window=image_window))
        self._layout.addLayout(AreaOfEffectControls(image_window=image_window))
        self._layout.addLayout(AppControlsLayout(image_window=image_window, app=app))

        # take focus away from the text area
        self.setFocus()

    def mousePressEvent(self, event):
        # user clicked in the blank space of the GUI, take focus away from other elements
        self.setFocus()
        super().mousePressEvent(event)

    def _create_container(self):
        container = QHBoxLayout()
        container.setSpacing(20)
        self._layout.addLayout(container)
        return container

    def add_column_initiative(self):
        container = QVBoxLayout()
        container.setSpacing(20)
        self._superlayout.addLayout(container)

        text_area = StyledTextEdit()
        text_area.setPlaceholderText("Display initiative order")
        container.addWidget(text_area)

        def read_text_area():
            text = text_area.toPlainText().strip()
            self.image_window.add_initiative(text)

        text_area.connect_text_changed_callback_with_timer(read_text_area)

        increase_font_button = StyledButton("+")
        decrease_font_button = StyledButton("-")
        move_button = StyledButton("move")

        increase_font_button.clicked.connect(
            lambda: self.image_window.initiative_change_font_size(by=2)
        )
        decrease_font_button.clicked.connect(
            lambda: self.image_window.initiative_change_font_size(by=-2)
        )
        move_button.clicked.connect(lambda: self.image_window.initiative_move())

        subcontainer = QHBoxLayout()
        subcontainer.setSpacing(20)
        container.addLayout(subcontainer)

        subcontainer.addWidget(increase_font_button)
        subcontainer.addWidget(decrease_font_button)
        subcontainer.addWidget(move_button)
