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
from battle_map_tv.layouts.initiative_controls import InitiativeControls
from battle_map_tv.widgets import get_window_icon
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

        self._superlayout.addLayout(InitiativeControls(image_window))

        layout = QVBoxLayout()
        self._superlayout.addLayout(layout)

        layout.addLayout(
            ImageButtonsLayout(image_window=image_window, default_directory=default_directory)
        )
        layout.addLayout(ImageScaleSlidersLayout(image_window=image_window))
        layout.addLayout(GridControls(image_window=image_window))
        layout.addLayout(AreaOfEffectControls(image_window=image_window))
        layout.addLayout(AppControlsLayout(image_window=image_window, app=app))

        # take focus away from the text area
        self.setFocus()

    def mousePressEvent(self, event):
        # user clicked in the blank space of the GUI, take focus away from other elements
        self.setFocus()
        super().mousePressEvent(event)
