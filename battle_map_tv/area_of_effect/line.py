import math
from typing import Optional

from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem

from battle_map_tv.area_of_effect.base_shape import BaseShape
from battle_map_tv.grid import Grid


class Line(BaseShape):
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        grid: Grid,
        scene: QGraphicsScene,
        size: Optional[float] = None,
    ):
        width = 20
        self.size = size or self._calculate_size(x1=x1, y1=y1, x2=x2, y2=y2, grid=grid)
        self.shape = QGraphicsRectItem(0, -width / 2, self.size, width)
        transform = QTransform()
        transform.translate(x1, y1)
        angle_radians = self._get_angle_radians(x1=x1, y1=y1, x2=x2, y2=y2, grid=grid)
        angle_degrees = math.degrees(angle_radians)
        transform.rotate(angle_degrees)
        self.shape.setTransform(transform)
        super().__init__(scene=scene)
