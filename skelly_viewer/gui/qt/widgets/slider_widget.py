from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtWidgets import QSlider, QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout

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

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        slider_hbox = QHBoxLayout()
        self._layout.addLayout(slider_hbox)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        slider_hbox.addWidget(self._slider)
        self._slider.setMaximum(0)
        self._slider.valueChanged.connect(lambda: self._frame_count_label.setText(str(self._slider.value())))

        self._frame_count_label = QLabel(f"Frame# {self._slider.value()}")

        slider_hbox.addWidget(self._frame_count_label)


        hbox = QHBoxLayout()
        self._layout.addLayout(hbox)

        self._play_button = QSliderButton("Play")
        self._play_button.clicked.connect(self._play_button_clicked)
        hbox.addWidget(self._play_button)

        self._play_double_speed_button = QSliderButton("Play x2")
        self._play_button.clicked.connect(self._play_double_speed_button_clicked)
        hbox.addWidget(self._play_double_speed_button)

        self._play_half_speed_button = QSliderButton("Play x1/2")
        self._play_button.clicked.connect(self._play_half_speed_button_clicked)
        hbox.addWidget(self._play_half_speed_button)

        self._pause_button = QSliderButton("Pause")
        self._pause_button.clicked.connect(self._pause_button_clicked)
        hbox.addWidget(self._pause_button)

        self._reset_button = QSliderButton("Reset")
        self._reset_button.clicked.connect(self._reset_button_clicked)
        hbox.addWidget(self._reset_button)




    @property
    def frames_per_second(self):
        return (1/PRESUMED_FRAMES_PER_SECOND)*1000
    @property
    def frame_duration(self):
        return 1/self.frames_per_second

    def set_slider_range(self,num_frames):
        self.slider_max = num_frames - 1
        self._slider.setValue(0)
        self._slider.setMaximum(self.slider_max)

    @pyqtSlot()
    def _timer_timeout(self):
        if self._slider.value() < self.slider_max:
            self._slider.setValue(self._slider.value() + 1)
        else:
            self._slider.setValue(0)

    @pyqtSlot()
    def _play_button_clicked(self):
        self._timer.stop()
        self._timer.start(int(self.frame_duration))

    @pyqtSlot()
    def _play_double_speed_button_clicked(self):
        self._timer.stop()
        self._timer.start(int(self.frame_duration/2))

    @pyqtSlot()
    def _play_half_speed_button_clicked(self):
        self._timer.stop()
        self._timer.start(int(self.frame_duration*2))

    @pyqtSlot()
    def _pause_button_clicked(self):
        self._timer.stop()

    @pyqtSlot()
    def _reset_button_clicked(self):
        self._timer.stop()
        self._slider.setValue(0)