from pathlib import Path

import cv2
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class VideoProcessingWorker():
    # this is a worker that handles all the video processing stuff - loading the videos as well as grabbing, converting, and displaying frames
    def __init__(self, video_path: Path):
        self.video_path = video_path
        self.video_capture_object = self.load_video_from_path()

    def load_video_from_path(self):
        # create an opencv object for the video
        video_capture_object = cv2.VideoCapture(str(self.video_path))
        return video_capture_object

    def increment_frame_number(self, frame_number: int):
        # whenever a frame number is given, set the video to the frame, read it out, and convert it to a pixmap
        self.set_video_to_frame(frame_number)
        frame = self.read_frame_from_video()
        self.pixmap = self.convert_frame_to_pixmap(frame)

    def set_video_to_frame(self, frame_number: int):
        self.video_capture_object.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def read_frame_from_video(self):
        ret, frame = self.video_capture_object.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def convert_frame_to_pixmap(self, frame):
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format.Format_RGB888)
        QtGui.QPixmap()
        pix = QtGui.QPixmap.fromImage(img)
        resized_pixmap = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
        return resized_pixmap

