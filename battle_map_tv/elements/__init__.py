import os

from PySide6.QtGui import QIcon


def get_window_icon():
    path = os.path.dirname(os.path.abspath(__file__))
    return QIcon(os.path.join(path, "icon.png"))
