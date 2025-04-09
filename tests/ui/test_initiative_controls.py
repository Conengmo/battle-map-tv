import time

from PySide6.QtCore import Qt

from battle_map_tv.layouts.initiative_controls import InitiativeTextArea
from battle_map_tv.utils import find_child_by_attribute


def test_initiative_text_area_updates_image_window(image_window, gui_window, qtbot):
    text_area = find_child_by_attribute(parent=gui_window, child_type=InitiativeTextArea)
    text_area.setFocus()
    assert len(image_window.initiative_overlay_manager.overlays) == 0

    # Simulate writing text in the text area
    qtbot.keyClicks(text_area, "Test Initiative Order")
    qtbot.wait(text_area.text_changed_debounce_ms * 2)
    assert len(image_window.initiative_overlay_manager.overlays) == 2

    # Simulate clearing the text area
    qtbot.keyClicks(text_area, "\b" * len("Test Initiative Order"))
    qtbot.wait(text_area.text_changed_debounce_ms * 2)
    assert len(image_window.initiative_overlay_manager.overlays) == 0
