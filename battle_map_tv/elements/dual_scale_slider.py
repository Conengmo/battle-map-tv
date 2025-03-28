from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout
from PySide6.QtCore import Signal

from ui_elements import StyledSlider, StyledLineEdit


class DualScaleSlider(QWidget):
    scale_changed = Signal(float)

    def __init__(self):
        super().__init__()

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Image scale:"))
        scale_layout.addSpacing(5)
        self.scale_edit = StyledLineEdit(max_length=10, width=120, value="1.00000")
        scale_layout.addWidget(self.scale_edit)
        scale_layout.addStretch()

        coarse_layout = QHBoxLayout()
        coarse_label = QLabel("Coarse")
        self.coarse_slider = StyledSlider(lower=1, upper=4000, default=1000)
        coarse_layout.addWidget(coarse_label)
        coarse_layout.addWidget(self.coarse_slider)

        fine_layout = QHBoxLayout()
        fine_label = QLabel("Fine")
        self.fine_slider = StyledSlider(lower=-10000, upper=10000, default=0)
        fine_layout.addWidget(fine_label)
        fine_layout.addWidget(self.fine_slider)

        grid_layout = QGridLayout()
        grid_layout.addWidget(coarse_label, 0, 0)
        grid_layout.addWidget(self.coarse_slider, 0, 1)
        grid_layout.addWidget(fine_label, 1, 0)
        grid_layout.addWidget(self.fine_slider, 1, 1)
        grid_layout.setColumnStretch(1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(scale_layout)
        main_layout.addSpacing(9)
        main_layout.addLayout(grid_layout)

        self.coarse_slider.valueChanged.connect(self.update_scale_from_sliders)
        self.fine_slider.valueChanged.connect(self.update_scale_from_sliders)
        self.scale_edit.editingFinished.connect(self.update_scale_from_edit)

    def update_scale_from_sliders(self):
        coarse_value = self.coarse_slider.value() / 1000
        fine_value = self.fine_slider.value() / 100000
        total_scale = coarse_value + fine_value

        self.scale_edit.setText(f"{total_scale:.5f}")

        self.scale_changed.emit(total_scale)

    def update_scale_from_edit(self):
        text = self.scale_edit.text()
        try:
            value = float(text)
        except ValueError:
            return
        self.scale_changed.emit(value)

    def update_values(self, value: float):
        self.scale_edit.setText(f"{value:.5f}")
