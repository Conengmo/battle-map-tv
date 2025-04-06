import math
from typing import Optional

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF
from PySide6.QtWidgets import QGraphicsPolygonItem, QGraphicsScene

from battle_map_tv.area_of_effect.base_shape import BaseShape
from battle_map_tv.grid import Grid


class Square(BaseShape):
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
        if size is not None:
            self.size = size
        else:
            self.size = self._calculate_size(x1=x1, y1=y1, x2=x2, y2=y2, grid=None) / math.sqrt(2)
            if grid.enable_snap:
                self.size = grid.normalize_size(size=self.size)
        angle = self._get_angle_radians(x1=x1, y1=y1, x2=x2, y2=y2, grid=grid)
        point_2 = (
            x1 + self.size * math.sqrt(2) * math.cos(angle),
            y1 + self.size * math.sqrt(2) * math.sin(angle),
        )
        point_1 = (
            x1 + self.size * math.cos(angle + math.pi / 4),
            y1 + self.size * math.sin(angle + math.pi / 4),
        )
        point_3 = (
            x1 + self.size * math.cos(angle - math.pi / 4),
            y1 + self.size * math.sin(angle - math.pi / 4),
        )
        self.shape = QGraphicsPolygonItem(
            QPolygonF.fromList([QPointF(*p) for p in [(x1, y1), point_1, point_2, point_3]])
        )
        super().__init__(scene=scene)
