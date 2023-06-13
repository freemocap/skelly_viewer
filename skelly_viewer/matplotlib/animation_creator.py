import logging
from pathlib import Path
from typing import Union

import cv2
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.backends.backend_agg import FigureCanvasAgg

from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.matplotlib.subplots.subplot_2d import Subplot2d
from skelly_viewer.matplotlib.subplots.subplot_3d import Subplot3d
from skelly_viewer.matplotlib.subplots.timeseries_subplot import TimeseriesSubplot
from skelly_viewer.matplotlib.subplots.video_subplot import VideoSubplot


mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

FRAME_INTERVAL = 1000 / 30


class AnimationCreator:
    def __init__(self,
                 recording_path: Union[str, Path], ):
        data_loader = DataLoader(recording_path)
        self.recording_name = Path(recording_path).name
        self.output_file = Path(recording_path) / f"{self.recording_name}_animation.mp4"
        self.fig = plt.figure()
        grid_spec = gridspec.GridSpec(2, 2,
                                      figure=self.fig,
                                      width_ratios=[1, 1],
                                      height_ratios=[3, 1],
                                      wspace=0.05,
                                      hspace=0.05)
        self.subplot_3d = Subplot3d(figure=self.fig,
                                    grid_spec=grid_spec,
                                    subplot_index=(0, 0),
                                    data_loader=data_loader)

        self.subplot_2d = Subplot2d(figure=self.fig,
                                    grid_spec=grid_spec,
                                    subplot_index=(1, 0),
                                    data_loader=data_loader)

        self.subplot_timeseries = TimeseriesSubplot(figure=self.fig,
                                                    grid_spec=grid_spec,
                                                    subplot_index=(1, 1),
                                                    data_loader=data_loader, )

        self.subplot_video = VideoSubplot(figure=self.fig,
                                          grid_spec=grid_spec,
                                          subplot_index=(0, 1),
                                          video_path=data_loader.get_video_path())

        self.number_of_frames = data_loader.number_of_frames
        self.animation = animation.FuncAnimation(self.fig, self.animate,
                                                 frames=self.number_of_frames,
                                                 interval=FRAME_INTERVAL,
                                                 blit=False)

        self.animation_running = True
        self.animation.event_source.stop()  # Initially stop the animation

        # # Initialize OpenCV VideoWriter
        # self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use another codec
        # self.video_writer = cv2.VideoWriter(str(Path(recording_path) / f"{self.recording_name}.mp4"),
        #                                     self.fourcc,
        #                                     30.0,
        #                                     (1000, 1000))


    def toggle_animation(self):
        if self.animation_running:
            self.animation.event_source.stop()
            self.animation_running = False
        else:
            self.animation.event_source.start()
            self.animation_running = True
    def animate(self, frame_number: Union[str, int]):
        self.fig.suptitle(f"{self.recording_name} - Frame {frame_number}")
        self.subplot_3d.animate(frame_number)
        self.subplot_2d.animate(frame_number)
        self.subplot_timeseries.animate(frame_number)
        self.subplot_video.animate(frame_number)



    def show(self):
        self.animation.event_source.start()
        plt.show()

    def save(self):
        self.animation.save(self.output_file, writer='ffmpeg', fps=30)


if __name__ == "__main__":
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"

    animator = AnimationCreator(recording_path = SAMPLE_DATA_PATH)
    animator.show()

    print("Saving animation...")
    animator.save()
    print("Animation saved!")
