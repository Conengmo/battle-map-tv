from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QImageReader, QMouseEvent
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

from battle_map_tv.area_of_effect.manager import AreaOfEffectManager
from battle_map_tv.grid import Grid, GridOverlay
from battle_map_tv.image import Image
from battle_map_tv.initiative import InitiativeOverlayManager
from battle_map_tv.storage import ImageKeys, StorageKeys, get_from_storage, get_image_from_storage
from battle_map_tv.widgets import get_window_icon


class ImageWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setObjectName("image_window")
        self.setWindowTitle("Battle Map TV")
        self.setWindowIcon(get_window_icon())
        self.setStyleSheet(
            """
            background-color: #000000;
            border: 0px
        """
        )
        self.setAlignment(Qt.AlignCenter)  # type: ignore[attr-defined]
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # type: ignore[attr-defined]
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # type: ignore[attr-defined]
        # allow for large size images
        QImageReader.setAllocationLimit(0)

        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, self.size().width(), self.size().height())
        self.setScene(scene)

        self.image: Optional[Image] = None
        self.grid = Grid()
        self.grid_overlay: Optional[GridOverlay] = None
        self.initiative_overlay_manager = InitiativeOverlayManager(scene=scene)
        self.area_of_effect_manager = AreaOfEffectManager(window=self, grid=self.grid)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def add_image(self, image_path: str):
        self.image = Image(
            image_path=image_path,
            scene=self.scene(),
            window_width_px=self.width(),
            window_height_px=self.height(),
        )
        if self.grid_overlay is not None:
            self.add_grid(color_value=self.grid_overlay.color_value)

    def remove_image(self):
        if self.image is not None:
            self.image.delete()
            self.image = None

    def restore_image(self):
        try:
            previous_image = get_from_storage(StorageKeys.previous_image)
        except KeyError:
            pass
        else:
            self.remove_image()
            self.add_image(image_path=previous_image)

    def center_image(self):
        if self.image is not None:
            self.image.center()

    def rotate_image(self):
        if self.image is not None:
            self.image.rotate()

    def autoscale_image(self):
        if self.image is not None:
            self.image.autoscale(grid=self.grid)

    def scale_image(self, value: int, dispatch_event: bool = False):
        if self.image is not None:
            self.image.scale(value, dispatch_event=dispatch_event)

    def add_grid(self, color_value: int):
        if self.grid_overlay is not None:
            self.remove_grid()
        if self.image is not None:
            pixels_per_square = get_image_from_storage(
                image_filename=self.image.image_filename,
                key=ImageKeys.grid_pixels_per_square,
                default=None,
            )
            if pixels_per_square:
                self.grid.set_size(pixels_per_square)
        self.grid_overlay = GridOverlay(window=self, grid=self.grid, color_value=color_value)
        self.grid.enable_snap = True

    def scale_grid(self, value: int):
        self.grid.set_size(value)
        if self.grid_overlay is not None:
            self.grid_overlay.reset()

    def change_grid_color(self, value: int):
        if self.grid_overlay is not None:
            self.grid_overlay.update_color(value)

    def remove_grid(self):
        if self.grid_overlay is not None:
            self.grid_overlay.delete()
            self.grid_overlay = None
            self.grid.enable_snap = False

    def add_initiative(self, text: str):
        self.initiative_overlay_manager.create(text=text)

    def initiative_change_font_size(self, by: int):
        self.initiative_overlay_manager.change_font_size(by=by)

    def initiative_move(self):
        self.initiative_overlay_manager.move()

    def remove_initiative(self):
        self.initiative_overlay_manager.clear()

    def add_area_of_effect(self, shape: str, callback: Callable):
        self.area_of_effect_manager.wait_for(
            shape=shape,
            callback=callback,
        )

    def cancel_area_of_effect(self):
        self.area_of_effect_manager.cancel()

    def toggle_rasterize_area_of_effect(self, enable: bool):
        self.area_of_effect_manager.rasterize = enable

    def area_of_effect_set_color(self, color: str):
        self.area_of_effect_manager.color = color

    def clear_area_of_effect(self):
        self.area_of_effect_manager.clear_all()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scene().setSceneRect(0, 0, self.size().width(), self.size().height())
        self.grid.calculate()
        if self.grid_overlay is not None:
            self.grid_overlay.reset()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():  # type: ignore[attr-defined]
            self.toggle_fullscreen()
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if not self.area_of_effect_manager.mouse_press_event(event):
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() != Qt.MouseButton.LeftButton:
            return
        if not self.area_of_effect_manager.mouse_move_event(event):
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.area_of_effect_manager.mouse_release_event(event):
            super().mouseReleaseEvent(event)
