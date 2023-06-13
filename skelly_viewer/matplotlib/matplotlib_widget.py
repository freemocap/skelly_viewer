import sys
from pathlib import Path
from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.matplotlib.animation_creator import AnimationCreator


class MatplotlibAnimation(QWidget):
    def __init__(self, recording_path: Union[str, Path], parent=None):
        super(MatplotlibAnimation, self).__init__(parent)

        # Create animation
        self.data_loader = DataLoader(SAMPLE_DATA_PATH)
        self.animation_creator = AnimationCreator(recording_path=recording_path)

        # Set up layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Create Play/Pause button
        self.playButton = QPushButton('Play/Pause')
        self.playButton.clicked.connect(self.toggle_animation)
        self.layout.addWidget(self.playButton)


        # # Create frame slider
        # self.frameSlider = QSlider(Qt.Orientation.Horizontal)
        # self.frameSlider.setRange(0, self.animation_creator.number_of_frames - 1)  # Frame numbers as range
        # self.frameSlider.valueChanged.connect(self.update_frame)
        # self.layout.addWidget(self.frameSlider)


        # Add animation to layout
        self.canvas = FigureCanvasQTAgg(self.animation_creator.fig)
        self.layout.addWidget(self.canvas)

    def toggle_animation(self):
        self.animation_creator.toggle_animation()

    def update_frame(self, value):
        self.animation_creator.animate(value)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"

    animation_widget = MatplotlibAnimation(recording_path=SAMPLE_DATA_PATH)
    animation_widget.show()
    sys.exit(app.exec())
