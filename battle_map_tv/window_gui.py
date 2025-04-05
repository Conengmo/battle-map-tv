from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QWidget,
    QApplication,
)

from battle_map_tv.area_of_effect import area_of_effect_shapes_to_class
from battle_map_tv.events import global_event_dispatcher, EventKeys
from battle_map_tv.elements import get_window_icon
from battle_map_tv.elements.widgets import ColorSelectionWindow
from battle_map_tv.elements.layouts import FixedRowGridLayout
from battle_map_tv.elements.sliders import StyledSlider, DualScaleSlider
from battle_map_tv.elements.buttons import StyledButton
from battle_map_tv.elements.text_based import StyledTextEdit
from battle_map_tv.window_image import ImageWindow
from battle_map_tv.grid import GridOverlayColor


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
        self.default_directory = default_directory

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

        self.add_row_image_buttons()
        self.add_row_scale_slider()
        self.add_row_grid()
        self.add_row_area_of_effect()
        self.add_row_app_controls()

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

    def add_row_app_controls(self):
        container = self._create_container()

        button = StyledButton("Fullscreen")
        button.clicked.connect(self.image_window.toggle_fullscreen)
        container.addWidget(button)

        button = StyledButton("Exit")
        button.clicked.connect(self.app.quit)
        container.addWidget(button)

    def add_row_image_buttons(self):
        container = self._create_container()

        def open_file_dialog():
            file_dialog = QFileDialog(
                caption="Select an image file",
                directory=self.default_directory,  # type: ignore[arg-type]
            )
            file_dialog.setFileMode(QFileDialog.ExistingFile)  # type: ignore[attr-defined]
            if file_dialog.exec_():
                selected_file = file_dialog.selectedFiles()[0]
                self.image_window.remove_image()
                self.image_window.add_image(image_path=selected_file)

        button = StyledButton("Add")
        button.clicked.connect(open_file_dialog)
        container.addWidget(button)

        button = StyledButton("Remove")
        button.clicked.connect(self.image_window.remove_image)
        container.addWidget(button)

        button = StyledButton("Restore")
        button.clicked.connect(self.image_window.restore_image)
        container.addWidget(button)

        def callback_button_center_image():
            if self.image_window.image is not None:
                self.image_window.image.center()

        button = StyledButton("Center")
        button.clicked.connect(callback_button_center_image)
        container.addWidget(button)

        def callback_button_rotate_image():
            if self.image_window.image is not None:
                self.image_window.image.rotate()

        button = StyledButton("Rotate")
        button.clicked.connect(callback_button_rotate_image)
        container.addWidget(button)

        def button_autoscale_callback():
            if self.image_window.image is not None:
                self.image_window.image.autoscale(grid=self.image_window.grid)

        button = StyledButton("Autoscale")
        button.clicked.connect(button_autoscale_callback)
        container.addWidget(button)

    def add_row_scale_slider(self):
        container = self._create_container()

        def slider_scale_callback(value: int):
            if self.image_window.image is not None:
                self.image_window.image.scale(value, dispatch_event=False)

        slider = DualScaleSlider()
        slider.scale_changed.connect(slider_scale_callback)
        container.addWidget(slider)

        global_event_dispatcher.add_handler(
            event_type=EventKeys.change_scale,
            handler=slider.update_sliders_from_scale,
        )

    def add_row_grid(self):
        container = self._create_container()

        label = QLabel("Grid scale")
        container.addWidget(label)

        def slider_grid_size_callback(value: int):
            self.image_window.grid.set_size(value)
            if self.image_window.grid_overlay is not None:
                self.image_window.grid_overlay.reset()

        slider_grid_size = StyledSlider(
            lower=10, upper=400, default=self.image_window.grid.pixels_per_square
        )
        slider_grid_size.valueChanged.connect(slider_grid_size_callback)
        container.addWidget(slider_grid_size)

        def slider_grid_color_callback(value: int):
            if self.image_window.grid_overlay is not None:
                self.image_window.grid_overlay.update_color(value)

        label = QLabel("Grid color")
        container.addWidget(label)

        slider_grid_color = StyledSlider(
            lower=GridOverlayColor.min, upper=GridOverlayColor.max, default=GridOverlayColor.default
        )
        slider_grid_color.valueChanged.connect(slider_grid_color_callback)
        container.addWidget(slider_grid_color)

        def toggle_grid_callback(value: bool):
            if self.image_window.grid_overlay is not None:
                self.image_window.remove_grid()
            else:
                self.image_window.add_grid(color_value=slider_grid_color.value())
            self.image_window.grid.enable_snap = value
            global_event_dispatcher.dispatch_event(EventKeys.toggle_grid, value)

        button = StyledButton("Toggle grid", checkable=True)
        button.clicked.connect(toggle_grid_callback)
        container.addWidget(button)

    def add_row_area_of_effect(self):
        container = self._create_container()

        color_selector = ColorSelectionWindow(callback=self.image_window.area_of_effect_set_color)
        container.addWidget(color_selector)

        def get_area_of_effect_callback(_shape: str, _button: StyledButton):
            def callback():
                self.image_window.cancel_area_of_effect()
                if _button.isChecked():
                    self.image_window.add_area_of_effect(
                        shape=_shape,
                        callback=lambda: _button.setChecked(False),
                    )
                    for i in range(grid_layout_shapes.count()):
                        _other_button = grid_layout_shapes.itemAt(i).widget()
                        if _other_button != _button:
                            _other_button.setChecked(False)  # type: ignore[attr-defined]

            return callback

        grid_layout_shapes = FixedRowGridLayout(rows=2)
        container.addLayout(grid_layout_shapes)

        for shape in area_of_effect_shapes_to_class.keys():
            button = StyledButton(shape.title(), checkable=True, padding_factor=0.7)
            button.clicked.connect(get_area_of_effect_callback(shape, button))
            grid_layout_shapes.add_widget(button)

        grid_layout_controls = FixedRowGridLayout(rows=2)
        container.addLayout(grid_layout_controls)

        button_rasterize = StyledButton("Rasterize", checkable=True)
        button_rasterize.clicked.connect(self.image_window.toggle_rasterize_area_of_effect)
        grid_layout_controls.addWidget(button_rasterize)

        def rasterize_button_callback_toggle_grid(value_grid: bool):
            button_rasterize.setEnabled(value_grid)
            if value_grid is False:
                button_rasterize.setChecked(False)
                self.image_window.toggle_rasterize_area_of_effect(False)

        button_rasterize.setEnabled(False)
        global_event_dispatcher.add_handler(
            EventKeys.toggle_grid, rasterize_button_callback_toggle_grid
        )

        button = StyledButton("Clear")
        button.clicked.connect(self.image_window.clear_area_of_effect)
        grid_layout_controls.addWidget(button)

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
