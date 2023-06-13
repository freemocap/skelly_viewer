from typing import Union

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from skelly_viewer.experimental.plotly.data_loader import DataLoader


class AnimationCreator:
    def __init__(self, data_by_frame):
        self.data_by_frame = data_by_frame
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Configure your axes properties here
        self.ax.set_xlim([-5000, 5000])
        self.ax.set_ylim([-5000, 5000])
        self.ax.set_zlim([-5000, 5000])

        self.anim = animation.FuncAnimation(self.fig, self.animate, frames=len(data_by_frame), interval=1000 / 30,
                                            blit=False)

    def animate(self, frame_number: Union[str, int]):
        self.ax.clear()

        # Extract body coordinates
        body = self.data_by_frame[str(frame_number)]["body"]
        x_data = np.array([point["x"] for point in body.values()])
        y_data = np.array([point["y"] for point in body.values()])
        z_data = np.array([point["z"] for point in body.values()])

        # Find max range of the data
        max_range = np.array(
            [x_data.max() - x_data.min(), y_data.max() - y_data.min(), z_data.max() - z_data.min()]).max() / 2.0

        # Find the mid points in the data
        mid_x = (x_data.max() + x_data.min()) * 0.5
        mid_y = (y_data.max() + y_data.min()) * 0.5
        mid_z = (z_data.max() + z_data.min()) * 0.5

        # Set the limits of x, y and z axes
        self.ax.set_xlim(mid_x - max_range, mid_x + max_range)
        self.ax.set_ylim(mid_y - max_range, mid_y + max_range)
        self.ax.set_zlim(mid_z - max_range, mid_z + max_range)

        self.ax.scatter(x_data, y_data, z_data, c='purple')

    def show(self):
        plt.show()


if __name__ == "__main__":
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    data_loader = DataLoader(SAMPLE_DATA_PATH)
    data_by_frame = data_loader.load_data_by_frame()

    anim_creator = AnimationCreator(data_by_frame)
    anim_creator.show()
