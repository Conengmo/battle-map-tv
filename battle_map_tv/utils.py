from typing import TYPE_CHECKING, Optional, Tuple

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


def get_image_window_size_px() -> Tuple[int, int]:
    image_window = get_image_window()
    return size_to_tuple(image_window.size())


def get_image_filename() -> Optional[str]:
    image_window = get_image_window()
    return image_window.image.image_filename if image_window.image else None
