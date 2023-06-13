from typing import Tuple, Union

from matplotlib import pyplot as plt, gridspec

from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.matplotlib.subplots.subplot_2d import Subplot2d
from skelly_viewer.matplotlib.subplots.subplot_3d import Subplot3d
from skelly_viewer.matplotlib.subplots.timeseries_subplot import TimeseriesSubplot
from skelly_viewer.matplotlib.subplots.video_subplot import VideoSubplot


class FigureMaker:
    def __init__(self,
                 data_loader: DataLoader,
                 frames: list,
                 figure_size: Tuple[int, int] = (12, 12),):
        self.figure = plt.figure(figsize=figure_size)
        grid_spec = gridspec.GridSpec(2, 2,
                                      figure=self.figure.figure,
                                      width_ratios=[1, 1],
                                      height_ratios=[3, 1],
                                      wspace=0.05,
                                      hspace=0.05)

        self.subplot_3d = Subplot3d(figure=self.figure,
                                    grid_spec=grid_spec,
                                    subplot_index=(0, 0),
                                    data_loader=data_loader)

        self.subplot_2d = Subplot2d(figure=self.figure,
                                    grid_spec=grid_spec,
                                    subplot_index=(1, 0),
                                    data_loader=data_loader)

        self.subplot_timeseries = TimeseriesSubplot(figure=self.figure,
                                                    frames=frames,
                                                    grid_spec=grid_spec,
                                                    subplot_index=(1, 1),
                                                    data_loader=data_loader)

        self.subplot_video = VideoSubplot(figure=self.figure,
                                          grid_spec=grid_spec,
                                          subplot_index=(0, 1),
                                          video_path=data_loader.get_video_path())


    def update_figure(self, frame_number: Union[str, int]):
        self.subplot_3d.animate(frame_number=frame_number)
        self.subplot_2d.animate(frame_number=frame_number)
        self.subplot_timeseries.animate(frame_number=frame_number)
        self.subplot_video.animate(frame_number=frame_number)

    def show(self):
        plt.show()
