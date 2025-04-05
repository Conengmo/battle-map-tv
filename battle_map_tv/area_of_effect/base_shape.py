import math
from typing import Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt, QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import (
    QAbstractGraphicsShapeItem,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
)

from battle_map_tv.grid import Grid


class BaseShape(QObject):
    shape: QAbstractGraphicsShapeItem
    label: QGraphicsTextItem
    label_background: QGraphicsRectItem
    size: float
    angle_snap_factor = 32 / 2 / math.pi

    on_right_click = Signal(object)

    def __init__(self, scene: QGraphicsScene):
        super().__init__()
        self.shape.mousePressEvent = self._mouse_press_event  # type: ignore[method-assign]
        self.scene = scene
        self.scene.addItem(self.shape)

    def remove(self):
        self.scene.removeItem(self.shape)
        try:
            self.scene.removeItem(self.label)
            self.scene.removeItem(self.label_background)
        except AttributeError:
            pass

    def _mouse_press_event(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.RightButton:  # type: ignore[attr-defined]
            self.remove()
            self.on_right_click.emit(self)

    def _get_angle_radians(self, x1: int, y1: int, x2: int, y2: int, grid: Grid) -> float:
        angle = math.atan2(y2 - y1, x2 - x1)
        if grid.enable_snap:
            angle = round(angle * self.angle_snap_factor) / self.angle_snap_factor
        return angle

    @staticmethod
    def _calculate_size(x1: int, y1: int, x2: int, y2: int, grid: Optional[Grid]) -> float:
        size = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if grid and grid.enable_snap:
            size = grid.normalize_size(size=size)
        return size

    def set_color(self, color):
        color_obj = QColor(color)
        pen = QPen(color_obj)
        pen.setWidth(3)
        self.shape.setPen(pen)
        color_obj.setAlpha(127)
        self.shape.setBrush(QBrush(color_obj))
        self.shape.setZValue(1)

    def set_is_movable(self):
        self.shape.setFlag(self.shape.GraphicsItemFlag.ItemIsMovable)

    def add_label(self, x: int, y: int, grid: Grid):
        self.label = QGraphicsTextItem()
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setDefaultTextColor(QColor("black"))

        value = grid.pixels_to_feet(self.size)
        self.label.setPlainText(f"{value:.0f}")

        self.label_background = QGraphicsRectItem(self.label.boundingRect())
        self.label_background.setBrush(QColor(255, 255, 255, 220))
        self.label_background.setPen(QColor(255, 255, 255, 255))

        self.label.setPos(x + 25, y + 15)
        self.label_background.setPos(self.label.pos())

        self.label.setZValue(3)
        self.label_background.setZValue(2)

        self.scene.addItem(self.label)
        self.scene.addItem(self.label_background)
