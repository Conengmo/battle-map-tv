import pytest
from PySide6.QtWidgets import QApplication

from battle_map_tv.window_gui import GuiWindow
from battle_map_tv.window_image import ImageWindow


@pytest.fixture
def app_instance(qtbot):
    app = QApplication.instance() or QApplication([])
    return app


@pytest.fixture
def image_window(app_instance, qtbot):
    image_window = ImageWindow()
    qtbot.addWidget(image_window)
    image_window.move(image_window.screen().geometry().center())
    yield image_window
    image_window.close()


@pytest.fixture
def gui_window(app_instance, image_window, qtbot):
    gui_window = GuiWindow()
    qtbot.addWidget(gui_window)
    gui_window.move(gui_window.screen().geometry().topLeft())
    yield gui_window
    gui_window.close()
