import math
import time

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore


class SpherePathGenerator:
    def __init__(self, number_of_spheres: int = 24):
        self.number_of_spheres = number_of_spheres

    def generate_path(self, time_factor: float):
        positions = np.zeros((self.number_of_spheres, 3))
        for i in range(self.number_of_spheres):
            angle = 2 * math.pi * i / self.number_of_spheres + time_factor
            positions[i, 0] = 10 * math.sin(angle)
            positions[i, 1] = 10 * math.cos(angle)
            positions[i, 2] = math.sin(2 * angle)
        return positions


class SpheresViewer:
    def __init__(self, sphere_path_generator: SpherePathGenerator):
        self.app = pg.mkQApp("GLScatterPlotItem Example")
        self.view_widget = gl.GLViewWidget()
        self.view_widget.setWindowTitle('pyqtgraph example: Connected Spheres')
        self.view_widget.setCameraPosition(distance=50)

        self.grid = gl.GLGridItem()
        self.view_widget.addItem(self.grid)

        self.path_generator = sphere_path_generator

        initial_pos = self.path_generator.generate_path(0)
        size = np.full(24, 1)
        color = np.array([[1.0, 0.0, 0.0, 0.5]] * 24)

        self.spheres_item = gl.GLScatterPlotItem(
            pos=initial_pos, size=size, color=color, pxMode=False
        )

        self.view_widget.addItem(self.spheres_item)

        self.start_time = time.time()

    def update(self):
        time_factor = (time.time() - self.start_time) * 0.1
        new_positions = self.path_generator.generate_path(time_factor)
        self.spheres_item.setData(pos=new_positions)

    def start(self):
        self.view_widget.show()
        update_timer = QtCore.QTimer()
        update_timer.timeout.connect(self.update)
        update_timer.start(50)
        pg.exec()


if __name__ == '__main__':
    generator = SpherePathGenerator()
    viewer = SpheresViewer(generator)
    viewer.start()