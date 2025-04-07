from typing import TYPE_CHECKING

from PySide6.QtWidgets import QLabel

from battle_map_tv.events import EventKeys, global_event_dispatcher
from battle_map_tv.grid import GridOverlayColor
from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.widgets.sliders import StyledSlider

if TYPE_CHECKING:
    from battle_map_tv.window_image import ImageWindow


class GridControls(HorizontalLayout):
    def __init__(self, image_window: "ImageWindow"):
        super().__init__()
        self.image_window = image_window

        label = QLabel("Grid scale")
        self.addWidget(label)

        slider_grid_size = StyledSlider(
            lower=10, upper=400, default=self.image_window.grid.pixels_per_square
        )
        slider_grid_size.valueChanged.connect(self.image_window.scale_grid)
        self.addWidget(slider_grid_size)

        label = QLabel("Grid color")
        self.addWidget(label)

        self.slider_grid_color = StyledSlider(
            lower=GridOverlayColor.min, upper=GridOverlayColor.max, default=GridOverlayColor.default
        )
        self.slider_grid_color.valueChanged.connect(self.image_window.change_grid_color)
        self.addWidget(self.slider_grid_color)

        self.add_button("Toggle grid", self.toggle_grid_callback, checkable=True)

    def toggle_grid_callback(self, value: bool):
        if value:
            self.image_window.add_grid(color_value=self.slider_grid_color.value())
        else:
            self.image_window.remove_grid()
        global_event_dispatcher.dispatch_event(EventKeys.toggle_grid, value)
