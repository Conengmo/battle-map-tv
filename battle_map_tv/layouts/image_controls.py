from typing import TYPE_CHECKING, Callable, Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout

from battle_map_tv.events import EventKeys, global_event_dispatcher
from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.widgets.sliders import StyledSlider
from battle_map_tv.widgets.text_based import StyledLineEdit

if TYPE_CHECKING:
    from battle_map_tv.window_image import ImageWindow


class ImageButtonsLayout(HorizontalLayout):
    """A horizontal layout with buttons to control the image."""

    def __init__(self, image_window: "ImageWindow", default_directory: Optional[str]):
        super().__init__()
        self.image_window = image_window
        self.default_directory = default_directory

        self.add_button("Add", self.add_image_callback)
        self.add_button("Remove", self.image_window.remove_image)
        self.add_button("Restore", self.image_window.restore_image)
        self.add_button("Center", self.image_window.center_image)
        self.add_button("Rotate", self.image_window.rotate_image)
        self.add_button("Autoscale", self.image_window.autoscale_image)

    def add_image_callback(self):
        file_dialog = QFileDialog(
            caption="Select an image file",
            directory=self.default_directory,  # type: ignore[arg-type]
        )
        file_dialog.setFileMode(QFileDialog.ExistingFile)  # type: ignore[attr-defined]
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.image_window.remove_image()
            self.image_window.add_image(image_path=selected_file)


class ImageScaleSlidersLayout(QVBoxLayout):
    """A horizontal layout with sliders to change the image scale."""

    scale_changed = Signal(float)

    factor_coarse = 1000
    factor_fine = 100000
    max_scale = 4

    def __init__(self, image_window: "ImageWindow"):
        super().__init__()
        self.image_window = image_window

        self.scale_changed.connect(self.image_window.scale_image)

        scale_layout = QHBoxLayout()
        scale_layout.setSpacing(5)
        scale_layout.addWidget(QLabel("Image scale:"))
        self.scale_edit = StyledLineEdit(max_length=10, width=120, value="1.00000")
        scale_layout.addWidget(self.scale_edit)
        scale_layout.addStretch()

        coarse_label = QLabel("Coarse")
        self.coarse_slider = StyledSlider(
            lower=1,
            upper=self.max_scale * self.factor_coarse,
            default=self.factor_coarse,
        )
        fine_label = QLabel("Fine")
        self.fine_slider = StyledSlider(
            lower=-self.factor_fine // 10,
            upper=self.factor_fine // 10,
            default=0,
        )

        sliders_labels_layout = QGridLayout()
        sliders_labels_layout.addWidget(coarse_label, 0, 0)
        sliders_labels_layout.addWidget(self.coarse_slider, 0, 1)
        sliders_labels_layout.addWidget(fine_label, 1, 0)
        sliders_labels_layout.addWidget(self.fine_slider, 1, 1)
        sliders_labels_layout.setColumnStretch(1, 1)

        self.setSpacing(9)
        self.addLayout(scale_layout)
        self.addLayout(sliders_labels_layout)

        self.coarse_slider.valueChanged.connect(self.update_scale_from_sliders)
        self.fine_slider.valueChanged.connect(self.update_scale_from_sliders)
        self.scale_edit.editingFinished.connect(self.update_scale_from_edit)

        global_event_dispatcher.add_handler(
            event_type=EventKeys.change_scale,
            handler=self.update_sliders_from_scale,
        )

    def update_scale_from_sliders(self):
        coarse_value = self.coarse_slider.value() / self.factor_coarse
        fine_value = self.fine_slider.value() / self.factor_fine
        total_scale = coarse_value + fine_value
        total_scale = self._value_bounds(total_scale)

        self.scale_edit.setText(f"{total_scale:.5f}")

        self.scale_changed.emit(total_scale)

    def update_scale_from_edit(self):
        text = self.scale_edit.text()
        try:
            value = float(text)
        except ValueError:
            return
        self.update_sliders_from_scale(value)

    def update_sliders_from_scale(self, value: float):
        coarse_value = round(self.factor_coarse * value)
        remainder = value - coarse_value / self.factor_coarse
        fine_value = round(self.factor_fine * remainder)
        self.coarse_slider.setValue(coarse_value)
        self.fine_slider.setValue(fine_value)

    def _value_bounds(self, value: float) -> float:
        return min(max(value, 1 / self.factor_fine), self.max_scale)
