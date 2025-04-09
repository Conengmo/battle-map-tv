from typing import Callable

from battle_map_tv.area_of_effect import area_of_effect_shapes_to_class
from battle_map_tv.events import EventKeys, global_event_dispatcher
from battle_map_tv.layouts.base import FixedRowGridLayout, HorizontalLayout
from battle_map_tv.utils import get_image_window
from battle_map_tv.widgets.buttons import ColorSelectionButton, StyledButton


class AreaOfEffectControls(HorizontalLayout):
    def __init__(self):
        super().__init__()
        self.image_window = get_image_window()

        color_selector = ColorSelectionWindow(callback=self.image_window.area_of_effect_set_color)
        self.addLayout(color_selector)

        self.addLayout(ShapeButtonsLayout())

        grid_layout_controls = FixedRowGridLayout(rows=2)
        self.addLayout(grid_layout_controls)

        self.button_rasterize = StyledButton("Rasterize", checkable=True)
        self.button_rasterize.clicked.connect(self.image_window.toggle_rasterize_area_of_effect)
        self.button_rasterize.setEnabled(False)
        grid_layout_controls.addWidget(self.button_rasterize)

        global_event_dispatcher.add_handler(
            EventKeys.toggle_grid,
            self.rasterize_button_callback_toggle_grid,
        )

        button = StyledButton("Clear")
        button.clicked.connect(self.image_window.clear_area_of_effect)
        grid_layout_controls.addWidget(button)

    def rasterize_button_callback_toggle_grid(self, value_grid: bool):
        self.button_rasterize.setEnabled(value_grid)
        if value_grid is False:
            self.button_rasterize.setChecked(False)
            self.image_window.toggle_rasterize_area_of_effect(False)


class ShapeButtonsLayout(FixedRowGridLayout):
    """A grid layout with buttons to select a shape to draw."""

    def __init__(self):
        super().__init__(rows=2)
        for shape in area_of_effect_shapes_to_class.keys():
            button = StyledButton(shape.title(), checkable=True, padding_factor=0.7)
            button.clicked.connect(self.get_area_of_effect_callback(shape, button))
            self.add_widget(button)

    def get_area_of_effect_callback(self, _shape: str, _button: StyledButton):
        image_window = get_image_window()

        def callback():
            image_window.cancel_area_of_effect()
            if _button.isChecked():
                image_window.add_area_of_effect(
                    shape=_shape,
                    callback=lambda: _button.setChecked(False),
                )
                for i in range(self.count()):
                    _other_button = self.itemAt(i).widget()
                    if _other_button != _button:
                        _other_button.setChecked(False)  # type: ignore[attr-defined]

        return callback


class ColorSelectionWindow(FixedRowGridLayout):
    def __init__(self, callback: Callable):
        super().__init__(rows=2)
        self.colors = [
            "#ff3d00",
            "#48ABB4",
            "#009E00",
            "#9702A7",
            "#FFF800",
            "grey",
            "black",
            "white",
        ]
        self.buttons = []
        for color in self.colors:
            button = ColorSelectionButton(color=color)
            button.clicked.connect(self.create_color_selected_handler(color, callback))
            self.add_widget(button)
            self.buttons.append(button)
        self.selected_color: str
        self.buttons[-1].click()

    def create_color_selected_handler(self, color: str, callback: Callable):
        def handler():
            self.selected_color = color
            for button in self.buttons:
                if button.color == color:
                    button.setStyleSheet(button.selected_stylesheet)
                else:
                    button.setStyleSheet(button.default_stylesheet)
            callback(color)

        return handler
