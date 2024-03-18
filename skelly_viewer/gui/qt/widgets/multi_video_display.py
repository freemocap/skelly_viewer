import logging
from collections import deque
from pathlib import Path
from typing import Union

import numpy as np
from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QApplication

from skelly_viewer.utilities.get_video_paths import get_video_paths
from skelly_viewer.utilities.video_handler import VideoHandler

logger = logging.getLogger(__name__)

MAX_COLUMN_COUNT = 2
MAX_BUFFER_LENGTH = 5


class UpdateDisplayWorker(QThread):
    updated = Signal(np.ndarray, int)

    def __init__(self, video_handlers):
        super().__init__()
        self.video_handlers = video_handlers
        self.buffer = deque(maxlen=MAX_BUFFER_LENGTH)

    def run(self):
        while True:
            for i, vh in enumerate(self.video_handlers):
                frame = vh.get_image_for_frame_number(vh.current_frame_number)
                self.buffer.append((frame, i))

                if len(self.buffer) == MAX_BUFFER_LENGTH:
                    for frame, video_number in self.buffer:
                        self.updated.emit(frame, video_number)

                    self.buffer.clear()


class MultiVideoDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.video_display_layout = QGridLayout()
        self._layout.addLayout(self.video_display_layout)

        self.update_worker = UpdateDisplayWorker([])

    def generate_video_display(self, path_to_video_folder: Union[str, Path]):
        self._video_handler_dictionary = self._create_video_handlers(get_video_paths(path_to_video_folder))
        self._image_label_widget_dictionary = self._create_image_label_widgets_for_videos(
            number_of_videos=len(self._video_handler_dictionary))
        self._remove_widets_from_layout()
        self._add_widgets_to_layout()

        self.update_worker.video_handlers = list(self._video_handler_dictionary.values())
        self.update_worker.updated.connect(self.update_display)

    def start_update_worker(self):
        self.update_worker.start()

    def stop_update_worker(self):
        self.update_worker.terminate()

    def update_display(self, frame_number: int):
        # logger.debug(f"Updating video display to frame#{frame_number}")
        try:
            for video_handler, image_label_widget in zip(self._video_handler_dictionary.values(),
                                                     self._image_label_widget_dictionary.values()):
                image = video_handler.get_image_for_frame_number(frame_number)
                self._set_pixmap_from_image(image_label_widget, image)

        except Exception as e:
            logger.warning(f"Error updating display for video {video_handler.video_path.name}: {e}")

    def _set_pixmap_from_image(self,
                               image_label_widget: QLabel,
                               image: np.ndarray):
        q_image = self._convert_image_to_qimage(image)
        pixmap = QPixmap.fromImage(q_image)

        image_label_widget_width = image_label_widget.width()
        image_label_widget_height = image_label_widget.height()

        scaled_width = int(image_label_widget_width * .95)
        scaled_height = int(image_label_widget_height * .95)

        pixmap = pixmap.scaled(
            scaled_width,
            scaled_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation, )

        image_label_widget.setPixmap(pixmap)

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


    def _create_image_label_widgets_for_videos(self, number_of_videos: int) -> object:
        label_widget_dictionary = {}
        for video_number in range(number_of_videos):
            label_widget_dictionary[video_number] = QLabel(f'Video {video_number}')
            label_widget_dictionary[video_number].setMinimumSize(200, 200)
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

    def _remove_widets_from_layout(self):
        """Removes all widgets from the video display layout"""
        # solution from here https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        for i in reversed(range(self.video_display_layout.count())): 
            self.video_display_layout.itemAt(i).widget().setParent(None)



if __name__ == '__main__':
    import sys


    app = QApplication(sys.argv)
    window = MultiVideoDisplay()
    window.show()
    sys.exit(app.exec())

