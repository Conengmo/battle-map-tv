from typing import TYPE_CHECKING, Callable, List, Optional, Tuple

from PySide6.QtGui import QMouseEvent, Qt

from battle_map_tv.area_of_effect import (
    area_of_effect_rasterized_shapes_to_class,
    area_of_effect_shapes_to_class,
)
from battle_map_tv.area_of_effect.base_shape import BaseShape
from battle_map_tv.grid import Grid

if TYPE_CHECKING:
    from battle_map_tv.window_image import ImageWindow


class AreaOfEffectManager:
    def __init__(self, window: "ImageWindow", grid: Grid):
        self.window = window
        self.scene = window.scene()
        self.grid = grid
        self._store: List[BaseShape] = []
        self.rasterize = False
        self.waiting_for: Optional[str] = None
        self.color = "white"
        self.start_point: Optional[Tuple[int, int]] = None
        self.temp_obj: Optional[BaseShape] = None
        self.callback: Optional[Callable] = None
        self._previous_size: Optional[float] = None

    def wait_for(self, shape: str, callback: Callable):
        self.waiting_for = shape
        self.callback = callback

    def cancel(self):
        if self.temp_obj is not None:
            self.temp_obj.remove()
            self.temp_obj = None
        self.waiting_for = None
        self.start_point = None
        self.callback = None

    def clear_all(self):
        for shape_obj in self._store:
            shape_obj.remove()
        self._store = []

    def mouse_press_event(self, event: QMouseEvent) -> bool:
        if self.waiting_for is not None:
            self.start_point = (event.pos().x(), event.pos().y())
            return True
        return False

    def mouse_move_event(self, event: QMouseEvent):
        if self.waiting_for is not None:
            if self.temp_obj is not None:
                self.temp_obj.remove()
            self.temp_obj = self._create_shape_obj(event=event)
            if self.grid.enable_snap:
                assert self.temp_obj
                self.temp_obj.add_label(x=event.pos().x(), y=event.pos().y(), grid=self.grid)
            return True
        return False

    def mouse_release_event(self, event: QMouseEvent) -> bool:
        if self.waiting_for is not None:
            assert self.callback
            shape_obj = self._create_shape_obj(event=event)
            shape_obj.set_is_movable()
            self._store.append(shape_obj)
            self.callback()
            self.cancel()
            return True
        return False

    def _create_shape_obj(self, event):
        assert self.waiting_for
        assert self.start_point
        shapes_dict = (
            area_of_effect_rasterized_shapes_to_class
            if self.rasterize
            else area_of_effect_shapes_to_class
        )
        shape_cls = shapes_dict[self.waiting_for]
        x1, y1 = self.start_point
        if self.grid.enable_snap:
            x1, y1 = self.grid.snap_to_grid(x=x1, y=y1)
        shape_obj = shape_cls(
            x1=x1,
            y1=y1,
            x2=event.pos().x(),
            y2=event.pos().y(),
            grid=self.grid,
            scene=self.scene,
            size=self._previous_size if event.modifiers() == Qt.ShiftModifier else None,  # type: ignore[attr-defined]
        )
        shape_obj.set_color(color=self.color)
        shape_obj.on_right_click.connect(lambda _shape: self._store.remove(_shape))
        self._previous_size = shape_obj.size
        return shape_obj
