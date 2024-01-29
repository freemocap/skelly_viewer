import logging
from pathlib import Path
from typing import Union

import cv2
import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)

class VideoHandler():
    # this is a worker that handles all the video processing stuff - loading the videos as well as grabbing, converting, and displaying frames
    def __init__(self, video_path: Path):
        self.video_path = video_path
        self.video_capture_object = self.load_video_from_path()

    def load_video_from_path(self):
        # create an opencv object for the video
        video_capture_object = cv2.VideoCapture(str(self.video_path))
        return video_capture_object

    def get_image_for_frame_number(self, frame_number: int)->np.ndarray:
        # whenever a frame number is given, set the video to the frame, read it out, and convert it to a pixmap
        self.set_video_to_frame(frame_number-1)
        image = self.read_frame_from_video()
        return image


    def set_video_to_frame(self, frame_number: int):
        self.video_capture_object.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def read_frame_from_video(self) ->Union[None, np.ndarray]:
        success, image = self.video_capture_object.read()
        if not success:
            logger.exception(f"Error reading image from {Path(self.video_path).name}")
            raise Exception


        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def _convert_frame_to_pixmap(self, image:np.ndarray):
        q_image = QtGui.QImage(image, image.shape[1], image.shape[0], QtGui.QImage.Format.Format_RGB888)
        QtGui.QPixmap()
        pix = QtGui.QPixmap.fromImage(q_image)
        resized_pixmap = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
        return resized_pixmap

