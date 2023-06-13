from typing import Union

import numpy as np
from matplotlib import pyplot as plt

from skelly_viewer.data_loader.data_loader import DataLoader

AXIS_LIMITS_INITIAL = [-2000, 2000]
AXIS_LIMITS_ANIMATION = [-3000, 3000]
PLOT_COLOR = 'purple'


class Axis3dView:
    def __init__(self,
                 figure: plt.Figure,
                 grid_spec: plt.GridSpec,
                 data_loader: DataLoader, ):
        self.ax = figure.add_subplot(grid_spec[0,0], projection='3d')
        self.set_axis_limits(AXIS_LIMITS_INITIAL)
        self.data_by_frame = data_loader.data_by_frame["data_by_frame"]
        self.data_by_trajectory = data_loader.data_by_trajectory
        self.info = data_loader.data_by_frame["info"]

    def set_axis_limits(self, limits: list):
        self.ax.set_xlim(limits)
        self.ax.set_ylim(limits)
        self.ax.set_zlim(limits)

    def clear(self):
        self.ax.clear()

    def animate(self, frame_number: Union[str, int]):
        self.clear()
        self.set_axis_limits(AXIS_LIMITS_ANIMATION)

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
        )
