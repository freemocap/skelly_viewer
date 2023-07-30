import math
import sys
import time

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt6 import QtWidgets
from pyqtgraph.Qt import QtCore


class SpherePathGenerator:
    def generate_path(self, number_of_spheres: int, time_factor: float):
        positions = np.zeros((number_of_spheres, 3))
        for i in range(number_of_spheres):
            angle = 2 * math.pi * i / number_of_spheres + time_factor
            positions[i, 0] = 10 * math.sin(angle)
            positions[i, 1] = 10 * math.cos(angle)
            positions[i, 2] = math.sin(2 * angle)
        return positions


class SpheresViewer:
    def __init__(self, sphere_path_generator: SpherePathGenerator, number_of_spheres: int = 24, start_frame: int = 0,
                 end_frame: int = 240):
        self.app = pg.mkQApp("GLScatterPlotItem Example")
        self.view_widget = gl.GLViewWidget()
        self.view_widget.setWindowTitle('pyqtgraph example: Connected Spheres')
        self.view_widget.setCameraPosition(distance=50)

        self.grid = gl.GLGridItem()
        self.view_widget.addItem(self.grid)

        self.path_generator = sphere_path_generator
        self.initial_pos = self.path_generator.generate_path(number_of_spheres, start_frame)


        # Make the spheres
        self.spheres_item = []
        for pos in self.initial_pos:
            sphere_mesh_data = gl.MeshData.sphere(rows=10, cols=20)
            m3 = gl.GLMeshItem(meshdata=sphere_mesh_data, color=(1.0, 0.0, 0.0, 0.5), drawEdges=True)
            m3.translate(*pos)
            self.spheres_item.append(m3)
            self.view_widget.addItem(m3)

        self.frame_range = range(start_frame, end_frame)
        self.current_frame = start_frame
        self.update_timer = QtCore.QTimer()
        self.slider = None

    def set_slider(self, slider):
        self.slider = slider

    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.frame_range[-1]:
            self.current_frame = self.frame_range[0]  # loop back to start if current_frame exceeds end_frame
        new_positions = self.path_generator.generate_path(len(self.spheres_item), self.current_frame)
        for i, pos in enumerate(new_positions):
            self.spheres_item[i].resetTransform()
            self.spheres_item[i].translate(*pos)

        if self.slider is not None:
            self.slider.setValue(self.current_frame)



    def start(self):
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(50)

    def stop(self):
        self.update_timer.stop()

    # Add functions to move to a specific frame
    def goto_frame(self, frame_idx: int):
        if frame_idx in self.frame_range:
            self.current_frame = frame_idx
            self.update()


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, viewer, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.viewer = viewer
        self.resize(800, 600)
        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        viewer_layout = QtWidgets.QVBoxLayout()
        viewer_layout.addWidget(self.viewer.view_widget)

        btn_layout = QtWidgets.QVBoxLayout()

        play_button = QtWidgets.QPushButton("Play")
        play_button.clicked.connect(self.viewer.start)
        btn_layout.addWidget(play_button)

        pause_button = QtWidgets.QPushButton("Pause")
        pause_button.clicked.connect(self.viewer.stop)
        btn_layout.addWidget(pause_button)

        slider_layout = QtWidgets.QVBoxLayout()

        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider.setMinimum(min(self.viewer.frame_range))
        slider.setMaximum(max(self.viewer.frame_range))
        slider.setTickInterval(1)
        slider.valueChanged[int].connect(self.viewer.goto_frame)
        slider_layout.addWidget(slider)

        self.viewer.set_slider(slider)

        main_layout.addLayout(viewer_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(slider_layout)

        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    generator = SpherePathGenerator()
    viewer = SpheresViewer(generator)

    app = QtWidgets.QApplication([])
    mainWin = MyMainWindow(viewer)
    mainWin.show()
    sys.exit(app.exec())