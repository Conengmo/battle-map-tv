from typing import TYPE_CHECKING, Tuple

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
    from battle_map_tv.window_image import ImageWindow


def size_to_tuple(size: QSize) -> Tuple[int, int]:
    return size.width(), size.height()


def get_current_application() -> QApplication:
    return QApplication.instance()  # type: ignore[return-value]


def get_image_window() -> "ImageWindow":
    app = get_current_application()
    for widget in app.topLevelWidgets():
        if widget.objectName() == "image_window":
            return widget  # type: ignore[return-value]
    raise RuntimeError("Could not find ImageWindow instance.")
