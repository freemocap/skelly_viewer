import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.matplotlib.animation_creator import AnimationCreator


class MatplotlibAnimation(QWidget):
    def __init__(self, data_loader: DataLoader,  parent=None):
        super(MatplotlibAnimation, self).__init__(parent)

        # Set up layout
        self.layout = QVBoxLayout(self)

        # Create Play/Pause button
        self.playButton = QPushButton('Play/Pause')

        self.playButton.clicked.connect(self.toggle_animation)

        self.layout.addWidget(self.playButton)

        # Create animation
        self.data_loader = DataLoader(SAMPLE_DATA_PATH)
        self.animation_creator = AnimationCreator(self.data_loader)

        # Add animation to layout
        self.canvas = FigureCanvasQTAgg(self.animation_creator.fig)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def toggle_animation(self):
        self.animation_creator.toggle_animation()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    data_loader = DataLoader(SAMPLE_DATA_PATH)
    animation_widget = MatplotlibAnimation(data_loader=data_loader)
    animation_widget.show()
    sys.exit(app.exec())
