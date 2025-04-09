from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from battle_map_tv.utils import find_child_by_attribute


def test_fullscreen_button(image_window, gui_window, qtbot):
    fullscreen_button = find_child_by_attribute(gui_window, QPushButton, "Fullscreen")
    assert fullscreen_button

    # Check if the fullscreen mode is toggled
    qtbot.mouseClick(fullscreen_button, Qt.LeftButton)  # type: ignore
    assert image_window.isFullScreen()

    # now click again to make it normal again
    qtbot.mouseClick(fullscreen_button, Qt.LeftButton)  # type: ignore
    assert not image_window.isFullScreen()
