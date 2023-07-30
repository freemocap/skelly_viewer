import math
import sys
import time

import numpy as np
import pyvista as pv
from PyQt6 import QtWidgets
from pyvistaqt import BackgroundPlotter


class SpherePathGenerator:
    def __init__(self, number_of_spheres: int = 24):
        self.number_of_spheres = number_of_spheres

    def generate_path(self, time_factor: float):
        positions = np.zeros((self.number_of_spheres, 3))
        self.angles = 2 * np.pi * np.arange(self.number_of_spheres) / self.number_of_spheres + time_factor
        positions[:, 0] = 10 * np.sin(self.angles)
        positions[:, 1] = 10 * np.cos(self.angles)
        positions[:, 2] = np.sin(2 * self.angles)
        return positions


class SpheresViewer:
    def __init__(self, sphere_path_generator: SpherePathGenerator):
        self.app = QtWidgets.QApplication(["PyVistaQt Plot"])
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.add_axes()
        self.path_generator = sphere_path_generator
        initial_pos = self.path_generator.generate_path(0)
        self.spheres = pv.PolyData(initial_pos)

        pv.set_plot_theme('document')
        self.spheres['radius'] = 1
        self.plotter.add_mesh(self.spheres, smooth_shading=True)

        self.start_time = time.time()

    def update(self):
        time_factor = (time.time() - self.start_time) * 0.1
        new_positions = self.path_generator.generate_path(time_factor)
        self.spheres.points = new_positions

    def start(self):
        self.plotter.add_callback(self.update)
        self.plotter.show()

    def stop(self):
        self.plotter.clear_callbacks()




if __name__ == '__main__':
    generator = SpherePathGenerator()
    viewer = SpheresViewer(generator)
    viewer.start()

    viewer.stop()
    viewer.start()
    sys.exit(viewer.app.exec())