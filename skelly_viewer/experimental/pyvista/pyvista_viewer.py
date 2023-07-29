import sys
import os
import numpy as np
import pyvista as pv
from qtpy import QtWidgets
from pyvistaqt import QtInteractor, MainWindow

class MyMainWindow(MainWindow):

    def __init__(self, parent=None, show=True, num_spheres: int = 3):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # allow adding a sphere
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_sphere_action = QtWidgets.QAction('Add Sphere', self)
        self.add_sphere_action.triggered.connect(self.add_sphere)
        meshMenu.addAction(self.add_sphere_action)

        # List to hold the spheres
        self.spheres = []

        # Add random spheres by default
        for _ in range(num_spheres):
            self.add_random_sphere()

        if show:
            self.show()

    def add_random_sphere(self):
        """Add a random sphere to the pyqt frame and connect with rods."""
        radius = np.random.uniform(0.1, 0.5)
        center = np.random.uniform(-1, 1, size=3)
        sphere = pv.Sphere(radius=radius, center=center)
        self.spheres.append(sphere)
        self.plotter.add_mesh(sphere, show_edges=True)

        # Connect the new sphere to existing spheres with rods
        for existing_sphere in self.spheres[:-1]:
            self.add_rod(existing_sphere.center, sphere.center)

        self.plotter.reset_camera()

    def add_sphere(self):
        """Add a default sphere to the pyqt frame."""
        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere, show_edges=True)
        self.plotter.reset_camera()

    def add_rod(self, start_point, end_point, radius=0.05):
        """Add a cylindrical rod between two points."""
        end_point = np.array(end_point)
        start_point = np.array(start_point)
        direction = end_point - start_point
        length = np.linalg.norm(direction)
        rod = pv.Cylinder(center=(start_point + end_point) / 2, direction=direction, radius=radius, height=length)
        self.plotter.add_mesh(rod)


if __name__ == '__main__':
    os.environ["QT_API"] = "pyqt6"
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec())
