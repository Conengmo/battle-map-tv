import math
from typing import Optional, List, Tuple

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF

from PySide6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsPolygonItem

from .base_shape import BaseShape
from battle_map_tv.grid import Grid


class Circle(BaseShape):
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
        self.size = size or self._calculate_size(x1=x1, y1=y1, x2=x2, y2=y2, grid=grid)
        self.shape = QGraphicsEllipseItem(
            x1 - self.size,
            y1 - self.size,
            2 * self.size,
            2 * self.size,
        )
        super().__init__(scene=scene)


class CircleRasterized(BaseShape):
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
        self.size: int = int(size or self._calculate_size(x1=x1, y1=y1, x2=x2, y2=y2, grid=grid))
        polygon = QPolygonF.fromList(
            [
                QPointF(*point)
                for point in circle_to_polygon(
                    x_center=x1, y_center=y1, radius=self.size, grid=grid
                )
            ]
        )
        self.shape = QGraphicsPolygonItem(polygon)
        super().__init__(scene=scene)


def circle_to_polygon(
    x_center: int, y_center: int, radius: int, grid: Grid
) -> List[Tuple[int, int]]:
    delta = grid.pixels_per_square
    radius = radius - radius % delta
    if radius < delta:
        return []
    elif radius < 2 * delta:
        return [
            (x_center + radius, y_center + radius),
            (x_center + radius, y_center - radius),
            (x_center - radius, y_center - radius),
            (x_center - radius, y_center + radius),
        ]

    edges = CircleEdges()
    start_point = (0, 0 + radius)
    edges.add_point(*start_point)
    x_prev, y_prev = start_point

    while True:
        x = x_prev + delta
        y_star = y_prev - delta

        y_circle_prev = math.sqrt(radius**2 - x_prev**2)
        y_circle = math.sqrt(radius**2 - x**2)

        surface = (x - x_prev) * (y_circle - y_star) + 0.5 * (x - x_prev) * (
            y_circle_prev - y_circle
        )

        if surface < 0.5 * delta**2:
            edges.add_point(x_prev, y_star)
            y = y_star
        else:
            y = y_prev

        if x > y:
            break
        edges.add_point(x, y)
        x_prev = x
        y_prev = y

    points = [(x + x_center, y + y_center) for x, y in edges.get_circle_line()]
    return points


class CircleEdges:
    def __init__(self):
        self._edges: List[List[Tuple[int, int]]] = [[] for _ in range(8)]

    def add_point(self, x: int, y: int):
        points_for_all_octants = [
            (x, y),
            (y, x),
            (y, -x),
            (x, -y),
            (-x, -y),
            (-y, -x),
            (-y, x),
            (-x, y),
        ]
        for i, point in enumerate(points_for_all_octants):
            self._edges[i].append(point)

    def get_circle_line(self) -> List[Tuple[int, int]]:
        final_points = []
        flip = False
        for edge in self._edges:
            if flip:
                edge = edge[::-1][1:]
            final_points.extend(edge)
            flip = False if flip else True
        return final_points
