from typing import Union

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import gridspec

from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.matplotlib.subplots.subplot_2d import Subplot2d
from skelly_viewer.matplotlib.subplots.subplot_3d import Subplot3d
from skelly_viewer.matplotlib.subplots.timeseries_subplot import TimeseriesSubplot

FRAME_INTERVAL = 1000 / 30


class AnimationCreator:
    def __init__(self, data_loader: DataLoader):
        self.fig = plt.figure()
        grid_spec = gridspec.GridSpec(2, 2, figure=self.fig)
        self.axis_3d = Subplot3d(figure=self.fig,
                                 grid_spec=grid_spec,
                                 subplot_index=(0, 0),
                                 data_loader=data_loader)
        self.axis_2d = Subplot2d(figure=self.fig,
                                 grid_spec=grid_spec,
                                 subplot_index=(1, 0),
                                 data_loader=data_loader)

        self.timeseries_ax = TimeseriesSubplot(figure=self.fig,
                                               grid_spec=grid_spec,
                                               subplot_index=(1, 1),
                                               data_loader=data_loader, )

        self.number_of_frames = data_loader.number_of_frames
        self.anim = animation.FuncAnimation(self.fig, self.animate,
                                            frames=self.number_of_frames,
                                            interval=FRAME_INTERVAL,
                                            blit=False)

    def animate(self, frame_number: Union[str, int]):
        self.axis_3d.animate(frame_number)
        self.axis_2d.animate(frame_number)
        self.timeseries_ax.animate(frame_number)

    def show(self):
        plt.show()


if __name__ == "__main__":
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    data_loader = DataLoader(SAMPLE_DATA_PATH)
    animator = AnimationCreator(data_loader)
    animator.show()
