from typing import TYPE_CHECKING, Callable, Optional

from PySide6.QtWidgets import QFileDialog

from battle_map_tv.events import EventKeys, global_event_dispatcher
from battle_map_tv.layouts.base import HorizontalLayout
from battle_map_tv.widgets.buttons import StyledButton
from battle_map_tv.widgets.sliders import DualScaleSlider

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


class ImageScaleSlidersLayout(HorizontalLayout):
    """A horizontal layout with sliders to change the image scale."""

    def __init__(self, image_window: "ImageWindow"):
        super().__init__()
        self.image_window = image_window

        slider = DualScaleSlider()
        slider.scale_changed.connect(self.image_window.scale_image)
        self.addWidget(slider)

        global_event_dispatcher.add_handler(
            event_type=EventKeys.change_scale,
            handler=slider.update_sliders_from_scale,
        )
