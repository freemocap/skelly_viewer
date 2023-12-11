from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import QSlider, QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout

PRESUMED_FRAMES_PER_SECOND = 30


class QSliderButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedWidth(75)


class PlayPauseCountSlider(QWidget):
    def __init__(self):
        super().__init__()

        self._timer = QTimer()
        self._timer.timeout.connect(self._timer_timeout)

        self._layout = QVBoxLayout(self)

        slider_hbox = QHBoxLayout()
        self._layout.addLayout(slider_hbox)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        slider_hbox.addWidget(self._slider)
        self.slider_max = 0
        self._slider.valueChanged.connect(lambda: self._frame_count_label.setText(f"Frame# {self._slider.value()}"))

        self._frame_count_label = QLabel(f"Frame# {self._slider.value()}")
        slider_hbox.addWidget(self._frame_count_label)

        hbox = QHBoxLayout()
        self._layout.addLayout(hbox)

        self._play_button = QSliderButton("Play")
        self._play_button.clicked.connect(self._play_button_clicked)
        hbox.addWidget(self._play_button)

        self._pause_button = QSliderButton("Pause")
        self._pause_button.clicked.connect(self._pause_button_clicked)
        hbox.addWidget(self._pause_button)

        self._reset_button = QSliderButton("Reset")
        self._reset_button.clicked.connect(self._reset_button_clicked)
        hbox.addWidget(self._reset_button)

        self.set_frames_per_second(PRESUMED_FRAMES_PER_SECOND)

    @property
    def frames_per_second(self):
        return self._frames_per_second

    @property
    def frame_duration(self):
        return self._frame_duration

    def set_frames_per_second(self, frames_per_second):
        self._frames_per_second = frames_per_second
        self._frame_duration = 1.0 / frames_per_second

    def set_slider_range(self, num_frames):
        self.slider_max = num_frames - 1
        self._slider.setValue(0)
        self._slider.setMaximum(self.slider_max)

    @Slot()
    def _timer_timeout(self):
        if self._slider.value() < self.slider_max:
            self._slider.setValue(self._slider.value() + 1)
        else:
            self._slider.setValue(0)

    @Slot()
    def _play_button_clicked(self):
        self._timer.stop()
        self._timer.start(0)  # play as fast as possible

    @Slot()
    def _pause_button_clicked(self):
        self._timer.stop()

    @Slot()
    def _reset_button_clicked(self):
        self._timer.stop()
        self._slider.setValue(0)
