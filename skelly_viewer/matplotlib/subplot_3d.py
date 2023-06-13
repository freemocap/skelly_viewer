from typing import Union

import numpy as np
from matplotlib import pyplot as plt

from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.data_wrangling.get_bounding_cube import get_bounding_cube

PLOT_COLOR = 'purple'
MARKER_SIZE = 10


class Subplot3d:
    def __init__(self,
                 figure: plt.Figure,
                 grid_spec: plt.GridSpec,
                 data_loader: DataLoader, ):
        self.ax = figure.add_subplot(grid_spec[0, 0], projection='3d')

        self.data_by_frame = data_loader.data_by_frame["data_by_frame"]
        self.data_by_trajectory = data_loader.data_by_trajectory
        self.info = data_loader.data_by_frame["info"]

        self.com_xyz = data_loader.center_of_mass_xyz

        self.axis_limits = get_bounding_cube(self.com_xyz)

        self.set_axis_limits()

    def set_axis_limits(self):
        self.ax.set_xlim(self.axis_limits["x"])
        self.ax.set_ylim(self.axis_limits["y"])
        self.ax.set_zlim(self.axis_limits["z"])

    def clear(self):
        self.ax.clear()

    def animate(self, frame_number: Union[str, int]):
        self.clear()
        self.set_axis_limits()

        body_parts = self.data_by_frame[str(frame_number)]["body"]
        connections = self.info["names_and_connections"]["body"]["connections"]
        body_parts_names = list(body_parts.keys())

        for connection in connections:
            self.draw_body_parts_connection(body_parts, body_parts_names, connection)

        self.scatter_body_parts(body_parts)

    def draw_body_parts_connection(self, body_parts: dict, body_parts_names: list, connection: tuple):
        x_values = [body_parts[body_parts_names[connection[0]]]['x'], body_parts[body_parts_names[connection[1]]]['x']]
        y_values = [body_parts[body_parts_names[connection[0]]]['y'], body_parts[body_parts_names[connection[1]]]['y']]
        z_values = [body_parts[body_parts_names[connection[0]]]['z'], body_parts[body_parts_names[connection[1]]]['z']]

        self.ax.plot(x_values, y_values, z_values, PLOT_COLOR)

    def scatter_body_parts(self, body_parts: dict):
        self.ax.scatter(
            np.array([point["x"] for point in body_parts.values()]),
            np.array([point["y"] for point in body_parts.values()]),
            np.array([point["z"] for point in body_parts.values()]),
            c=PLOT_COLOR,
            s=MARKER_SIZE,
        )
