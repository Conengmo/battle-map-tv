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
    """The control window."""

    def __init__(self, image_window: ImageWindow, app: QApplication):
        super().__init__()
        self.setWindowTitle("Controls")
        self.setWindowIcon(get_window_icon())
        self.setStyleSheet(
            """
            background-color: #000000;
            color: #E5E5E5;
            font-size: 18px;
        """
        )
        self.setLayout(ControlsLayout(image_window, app))

        # take focus away from the text area
        self.setFocus()

    def mousePressEvent(self, event):
        # user clicked in the blank space of the GUI, take focus away from other elements
        self.setFocus()
        super().mousePressEvent(event)


class ControlsLayout(QHBoxLayout):
    """Main layout of the control window."""

    def __init__(self, image_window: "ImageWindow", app: QApplication):
        super().__init__()
        self.setAlignment(Qt.AlignVCenter)  # type: ignore[attr-defined]
        self.setContentsMargins(60, 80, 80, 80)
        self.setSpacing(50)

        self.addLayout(InitiativeControls(image_window))
        self.addLayout(RightColumnControls(image_window, app))


class RightColumnControls(QVBoxLayout):
    """Controls on the right-hand side of the control window."""

    def __init__(self, image_window: "ImageWindow", app: QApplication):
        super().__init__()
        self.addLayout(ImageButtonsLayout(image_window=image_window))
        self.addLayout(ImageScaleSlidersLayout(image_window=image_window))
        self.addLayout(GridControls(image_window=image_window))
        self.addLayout(AreaOfEffectControls(image_window=image_window))
        self.addLayout(AppControlsLayout(image_window=image_window, app=app))
