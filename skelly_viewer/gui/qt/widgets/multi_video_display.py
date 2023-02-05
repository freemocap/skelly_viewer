import logging
from pathlib import Path
from typing import Union

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QGridLayout, QSizePolicy

from skelly_viewer.utilities.video_handler import VideoHandler

logger = logging.getLogger(__name__)

MAX_COLUMN_COUNT = 2

class MultiVideoDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.video_display_layout = QGridLayout()
        self._layout.addLayout(self.video_display_layout)


    def generate_video_display(self, path_to_video_folder: Union[str, Path]):
        self._video_handler_dictionary = self._create_video_handlers(list(Path(path_to_video_folder).glob('*.mp4')))
        self._image_label_widget_dictionary = self._create_image_label_widgets_for_videos(number_of_videos =len(self._video_handler_dictionary))
        self._add_widgets_to_layout()

    def update_display(self, frame_number: int):
        # logger.debug(f"Updating video display to frame#{frame_number}")
        for video_handler, image_label_widget in zip(self._video_handler_dictionary.values(),
                                                     self._image_label_widget_dictionary.values()):
            image = video_handler.get_image_for_frame_number(frame_number)
            pixmap = self._set_pixmap_from_image(image_label_widget, image)


    def _set_pixmap_from_image(self,
                               image_label_widget:QLabel,
                                        image:np.ndarray):
        q_image = self._convert_image_to_qimage(image)

        image_label_widget_width = image_label_widget.width()
        image_label_widget_height = image_label_widget.height()

        scaled_width = int(image_label_widget_width * .95)
        scaled_height = int(image_label_widget_height * .95)

        q_image = q_image.scaled(
            scaled_width,
            scaled_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation, )

        image_label_widget.setPixmap(QPixmap.fromImage(q_image))

    def _convert_image_to_qimage(self, image: np.ndarray):
        return QImage(
            image.data,
            image.shape[1],
            image.shape[0],
            QImage.Format.Format_RGB888,
        )

    def _create_video_handlers(self, list_of_video_paths: list):
        # for every video, create a worker that can handle the video processing and add it to the dictionary
        self._video_handler_dictionary = {}

        for count, video_path in enumerate(list_of_video_paths):
            self._video_handler_dictionary[count] = VideoHandler(video_path)

        return self._video_handler_dictionary


    def _create_image_label_widgets_for_videos(self, number_of_videos: int):
        label_widget_dictionary = {}
        for video_number in range(number_of_videos):
            label_widget_dictionary[video_number] = QLabel(f'Video {video_number}')
            label_widget_dictionary[video_number].setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return label_widget_dictionary

    def _add_widgets_to_layout(self):
        column_count = 0
        row_count = 0
        for widget in self._image_label_widget_dictionary:
            self.video_display_layout.addWidget(self._image_label_widget_dictionary[widget], row_count, column_count)

            # This section is for formatting the videos in the grid nicely - it fills out two columns and then moves on to the next row
            column_count += 1
            if column_count % MAX_COLUMN_COUNT == 0:
                column_count = 0
                row_count += 1

