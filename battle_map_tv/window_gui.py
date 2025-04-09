from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
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


class GuiWindow(QWidget):
    """The control window."""

    def __init__(self):
        super().__init__()
        self.setObjectName("gui_window")
        self.setWindowTitle("Controls")
        self.setWindowIcon(get_window_icon())
        self.setStyleSheet(
            """
            background-color: #000000;
            color: #E5E5E5;
            font-size: 18px;
        """
        )
        self.setLayout(ControlsLayout())

        # take focus away from the text area
        self.setFocus()

    def mousePressEvent(self, event):
        # user clicked in the blank space of the GUI, take focus away from other elements
        self.setFocus()
        super().mousePressEvent(event)


class ControlsLayout(QHBoxLayout):
    """Main layout of the control window."""

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignVCenter)  # type: ignore[attr-defined]
        self.setContentsMargins(60, 80, 80, 80)
        self.setSpacing(50)

        self.addLayout(InitiativeControls())
        self.addLayout(RightColumnControls())


class RightColumnControls(QVBoxLayout):
    """Controls on the right-hand side of the control window."""

    def __init__(self):
        super().__init__()
        self.addLayout(ImageButtonsLayout())
        self.addLayout(ImageScaleSlidersLayout())
        self.addLayout(GridControls())
        self.addLayout(AreaOfEffectControls())
        self.addLayout(AppControlsLayout())
