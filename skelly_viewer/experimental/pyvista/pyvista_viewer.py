import sys
import os
import numpy as np
import pyvista as pv
from PyQt6.QtWidgets import QToolButton
from qtpy import QtWidgets
from pyvistaqt import QtInteractor, MainWindow
from PyQt6.QtCore import QTimer

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

        # Play/Pause button
        playMenu = mainMenu.addMenu('Play')
        self.play_action = QtWidgets.QAction('Play', self)
        self.play_action.triggered.connect(self.toggle_play)
        playMenu.addAction(self.play_action)

        # allow adding a sphere
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_sphere_action = QtWidgets.QAction('Add Sphere', self)
        self.add_sphere_action.triggered.connect(self.add_sphere)
        meshMenu.addAction(self.add_sphere_action)

        # List to hold the spheres
        self.spheres = []

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_spheres)
        self.timer.setInterval(33)  # 33 milliseconds

        # Add random spheres by default
        for _ in range(num_spheres):
            self.add_random_sphere()
        # Toolbar
        self.toolbar = self.addToolBar('Toolbar')
        # Play/Pause button
        self.play_button = QToolButton(self)
        self.play_button.setText('Play')
        self.play_button.clicked.connect(self.toggle_play)
        self.toolbar.addWidget(self.play_button)


        if show:
            self.show()

    def toggle_play(self):
        """Toggle play/pause for the animation."""
        if self.play_action.text() == "Play":
            self.play_action.setText("Pause")
            self.timer.start()
        else:
            self.play_action.setText("Play")
            self.timer.stop()

    def animate_spheres(self):
        """Update the sphere centers with random values and redraw the rods."""
        # Update the sphere centers
        for sphere in self.spheres:
            sphere.center += np.random.uniform(-0.05, 0.05, size=3)

        # Remove all existing rods
        for actor in self.plotter.renderer.actors:
            self.plotter.remove_actor(actor)

        # Add the spheres and rods based on the updated centers
        for sphere in self.spheres:
            self.plotter.add_mesh(sphere, show_edges=True)

        # Connect the spheres with rods
        for i, sphere in enumerate(self.spheres[:-1]):
            for next_sphere in self.spheres[i + 1:]:
                self.add_rod(sphere.center, next_sphere.center)

        self.plotter.update()

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
        start_point = np.array(start_point)
        end_point = np.array(end_point)
        direction = end_point - start_point
        length = np.linalg.norm(direction)
        rod = pv.Cylinder(center=(start_point + end_point) / 2, direction=direction, radius=radius, height=length)
        self.plotter.add_mesh(rod)


if __name__ == '__main__':
    os.environ["QT_API"] = "pyqt6"
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec())
