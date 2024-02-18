import pytest

from battle_map_tv.ui_elements import InitiativeOverlay


@pytest.mark.parametrize(
    "text, expected",
    [
        ("3 abc\n12 def\n1 ghi\n", " 1 ghi\n 3 abc\n12 def"),
        ("x\n  z\n\n\ny  \n", "x\ny\nz"),
        ("12 1 a\n13 b\n12 2 c", "12 1 a\n12 2 c\n13 b"),
    ],
)
def test_initiative_overlay_format_text(text, expected):
    result = InitiativeOverlay._format_text(text)
    assert result == expected
