from typing import Union, List

import numpy as np
from matplotlib.artist import Artist

from skelly_viewer.matplotlib.subplots.base_subplot import BasePlot, PLOT_COLOR, MARKER_SIZE

CAMERA_AZIMUTH = 0
CAMERA_ELEVATION = 0

class Subplot3d(BasePlot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis = self.figure.add_subplot(self.grid_spec[0, 0], projection='3d')
        self.set_axis_limits()

    def clear(self):
        self.axis.clear()

    def set_azimuth(self, angle: Union[str, int]):
        self.axis.azim = angle
    def set_elevation(self, angle: Union[str, int]):
        self.axis.elev = angle

    def set_axis_limits(self):
        self.axis.set_xlim(self.axis_limits["x"])
        self.axis.set_ylim(self.axis_limits["y"])
        self.axis.set_zlim(self.axis_limits["z"])

    def draw_body_parts_connection(self, body_parts: dict, body_parts_names: list, connection: tuple):
        x_values = [body_parts[body_parts_names[connection[0]]]['x'], body_parts[body_parts_names[connection[1]]]['x']]
        y_values = [body_parts[body_parts_names[connection[0]]]['y'], body_parts[body_parts_names[connection[1]]]['y']]
        z_values = [body_parts[body_parts_names[connection[0]]]['z'], body_parts[body_parts_names[connection[1]]]['z']]
        return self.axis.plot(x_values, y_values, z_values, PLOT_COLOR)

    def body_parts_scatter(self, body_parts: dict):
        return self.axis.scatter(
            np.array([point["x"] for point in body_parts.values()]),
            np.array([point["y"] for point in body_parts.values()]),
            np.array([point["z"] for point in body_parts.values()]),
            c=PLOT_COLOR,
            s=MARKER_SIZE,
        )

    def center_of_mass_scatter(self, center_of_mass_xyz: np.ndarray):
        return self.axis.scatter(
            center_of_mass_xyz[0],
            center_of_mass_xyz[1],
            center_of_mass_xyz[2],
            c='r',
            s=30,
        )


    def center_of_mass_trajectory(self, frame_number: int, tail_length: int = 30):
        start_frame = max(0, frame_number - tail_length)
        com_trajectory_slice = self.com_xyz[start_frame:frame_number, :]

        self.axis.plot3(
            com_trajectory_slice[:, 0],
            com_trajectory_slice[:, 1],
            com_trajectory_slice[:, 2],
            c='r',
        )

    # def center_of_mass_trajectory_2d(self, frame_number: int, tail_length: int = 30):
    #     start_frame = max(0, frame_number - tail_length)
    #     com_trajectory_slice = self.com_xyz[start_frame:frame_number, :]
    #
    #     self.axis.plot(
    #         com_trajectory_slice[:, 0],
    #         com_trajectory_slice[:, 1],
    #         c='r',
    #     )

    def animate(self, frame_number: Union[str, int])->List[Artist]:
        self.clear()
        self.set_axis_limits()
        self.set_azimuth(CAMERA_AZIMUTH)
        self.set_elevation(CAMERA_ELEVATION)
        body_parts = self.data_by_frame[str(frame_number)]["body"]
        connections = self.info["names_and_connections"]["body"]["connections"]
        body_parts_names = list(body_parts.keys())

        artists = []  # list to store all artists
        for connection in connections:
            self.draw_body_parts_connection(body_parts, body_parts_names, connection)
        artists.append(self.body_parts_scatter(body_parts))
        artists.append(self.center_of_mass_scatter(self.com_xyz[int(frame_number), :]))

        return artists
