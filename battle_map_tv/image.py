import os.path
from typing import Tuple

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

from battle_map_tv.events import global_event_dispatcher, EventKeys
from battle_map_tv.grid import Grid
from battle_map_tv.scale_detection import find_image_scale
from battle_map_tv.storage import (
    set_image_in_storage,
    ImageKeys,
    get_image_from_storage,
    set_in_storage,
    StorageKeys,
)


class CustomGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, image_path: str):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            raise ValueError(f"Failed to load '{image_path}'")
        super().__init__(pixmap)
        self.image_filename = os.path.basename(image_path)
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)

    def wheelEvent(self, event):
        value = self.scale() + event.delta() / 1500
        self.set_scale(value)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.store_position()

    def set_position(self, position: Tuple[int, int]):
        self.setPos(
            position[0] - self.pixmap().width() // 2,
            position[1] - self.pixmap().height() // 2,
        )
        self.store_position()

    def store_position(self):
        position = (
            self.pos().x() + self.pixmap().width() // 2,
            self.pos().y() + self.pixmap().height() // 2,
        )
        set_image_in_storage(self.image_filename, ImageKeys.position, position)

    def set_scale(self, value: float, dispatch_event: bool = True):
        self.setScale(value)
        if dispatch_event:
            global_event_dispatcher.dispatch_event(EventKeys.change_scale, value)
        set_image_in_storage(self.image_filename, ImageKeys.scale, value)


class Image:
    def __init__(
        self,
        image_path: str,
        scene: QGraphicsScene,
        window_width_px: int,
        window_height_px: int,
    ):
        self.rotation = 0

        image_path = os.path.abspath(image_path)
        self.filepath: str = image_path
        self.image_filename = os.path.basename(image_path)
        set_in_storage(key=StorageKeys.previous_image, value=image_path)

        self.scene = scene

        self.pixmap_item = CustomGraphicsPixmapItem(image_path)
        self.scene.addItem(self.pixmap_item)

        try:
            self.rotation = get_image_from_storage(
                self.image_filename,
                ImageKeys.rotation,
            )
        except KeyError:
            pass
        else:
            self.pixmap_item.setRotation(self.rotation)

        try:
            scale = get_image_from_storage(
                self.image_filename,
                ImageKeys.scale,
            )
        except KeyError:
            self._fit_image_to_window(window_width_px, window_height_px)
        else:
            self.scale(scale)

        try:
            position = get_image_from_storage(
                self.image_filename,
                ImageKeys.position,
            )
        except KeyError:
            self.center()
        else:
            self.pixmap_item.set_position(position)

    def _fit_image_to_window(self, window_width_px: int, window_height_px: int):
        image_width = self.pixmap_item.pixmap().width()
        image_height = self.pixmap_item.pixmap().height()
        scale = min(window_width_px / image_width, window_height_px / image_height)
        self.scale(scale)

    def delete(self):
        self.scene.removeItem(self.pixmap_item)

    def center(self):
        position = (int(self.scene.width() // 2), int(self.scene.height() // 2))
        self.pixmap_item.set_position(position)

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360
        self.pixmap_item.setRotation(self.rotation)
        set_image_in_storage(self.image_filename, ImageKeys.rotation, self.rotation)

    def scale(self, value: float, dispatch_event: bool = True):
        self.pixmap_item.set_scale(value, dispatch_event=dispatch_event)

    def autoscale(self, grid: Grid):
        image_px_per_square = find_image_scale(self.filepath)
        scale = grid.pixels_per_square / image_px_per_square
        self.scale(scale)
