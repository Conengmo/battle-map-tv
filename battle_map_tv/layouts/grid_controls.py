from battle_map_tv.events import EventKeys, global_event_dispatcher
from battle_map_tv.grid import GridOverlayColor
from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.utils import get_image_window
from battle_map_tv.widgets.sliders import StyledSlider


class GridControls(HorizontalLayout):
    def __init__(self):
        super().__init__()
        self.image_window = get_image_window()

        self.add_label("Grid scale")

        slider_grid_size = StyledSlider(
            lower=10, upper=400, default=self.image_window.grid.pixels_per_square
        )
        slider_grid_size.valueChanged.connect(self.image_window.scale_grid)
        self.addWidget(slider_grid_size)

        self.add_label("Grid color")

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
