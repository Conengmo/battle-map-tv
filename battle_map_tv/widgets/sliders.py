from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget

from battle_map_tv.widgets.text_based import StyledLineEdit


class DualScaleSlider(QWidget):
    scale_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self.factor_coarse = 1000
        self.factor_fine = 100000
        self.max_scale = 4

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Image scale:"))
        scale_layout.addSpacing(5)
        self.scale_edit = StyledLineEdit(max_length=10, width=120, value="1.00000")
        scale_layout.addWidget(self.scale_edit)
        scale_layout.addStretch()

        coarse_label = QLabel("Coarse")
        self.coarse_slider = StyledSlider(
            lower=1,
            upper=self.max_scale * self.factor_coarse,
            default=self.factor_coarse,
        )
        fine_label = QLabel("Fine")
        self.fine_slider = StyledSlider(
            lower=-self.factor_fine // 10,
            upper=self.factor_fine // 10,
            default=0,
        )

        sliders_labels_layout = QGridLayout()
        sliders_labels_layout.addWidget(coarse_label, 0, 0)
        sliders_labels_layout.addWidget(self.coarse_slider, 0, 1)
        sliders_labels_layout.addWidget(fine_label, 1, 0)
        sliders_labels_layout.addWidget(self.fine_slider, 1, 1)
        sliders_labels_layout.setColumnStretch(1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(scale_layout)
        main_layout.addSpacing(9)
        main_layout.addLayout(sliders_labels_layout)

        self.coarse_slider.valueChanged.connect(self.update_scale_from_sliders)
        self.fine_slider.valueChanged.connect(self.update_scale_from_sliders)
        self.scale_edit.editingFinished.connect(self.update_scale_from_edit)

    def update_scale_from_sliders(self):
        coarse_value = self.coarse_slider.value() / self.factor_coarse
        fine_value = self.fine_slider.value() / self.factor_fine
        total_scale = coarse_value + fine_value
        total_scale = self._value_bounds(total_scale)

        self.scale_edit.setText(f"{total_scale:.5f}")

        self.scale_changed.emit(total_scale)

    def update_scale_from_edit(self):
        text = self.scale_edit.text()
        try:
            value = float(text)
        except ValueError:
            return
        self.update_sliders_from_scale(value)

    def update_sliders_from_scale(self, value: float):
        coarse_value = round(self.factor_coarse * value)
        remainder = value - coarse_value / self.factor_coarse
        fine_value = round(self.factor_fine * remainder)
        self.coarse_slider.setValue(coarse_value)
        self.fine_slider.setValue(fine_value)

    def _value_bounds(self, value: float) -> float:
        return min(max(value, 1 / self.factor_fine), self.max_scale)


class StyledSlider(QSlider):
    def __init__(self, lower: int, upper: int, default: int, *args, **kwargs):
        super().__init__(Qt.Horizontal, *args, **kwargs)  # type: ignore[attr-defined]
        self.setMinimum(lower)
        self.setMaximum(upper)
        self.setValue(default)
        self.setStyleSheet(
            """
            QSlider {
                height: 40px;
            }
            QSlider::groove:horizontal {
                height: 10px;
                background: #404040;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background: #717173;
                border: 1px solid #3E3E40;
                width: 20px;
                margin: -15px 0;
                border-radius: 6px;
            }
        """
        )
