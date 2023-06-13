from pathlib import Path
from typing import Union

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

class VideoSubplot:
    def __init__(self,
                 figure: Figure,
                 grid_spec: GridSpec,
                 subplot_index: tuple,
                 video_path: Union[str, Path]):
        self.figure = figure
        self.grid_spec = grid_spec
        self.subplot_index = subplot_index
        self.ax = self.figure.add_subplot(self.grid_spec[self.subplot_index[0], self.subplot_index[1]])
        self.video_path = video_path
        self.cap = cv2.VideoCapture(str(video_path))

    def clear(self):
        self.ax.clear()

    def animate(self, frame_number):
        self.clear()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if ret:
            # Convert the BGR image to RGB, then display it
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.ax.imshow(frame)
            self.ax.axis('off')  # Hide axes
        else:
            print(f"Unable to retrieve frame {frame_number} from video")

    def __del__(self):
        self.cap.release()
