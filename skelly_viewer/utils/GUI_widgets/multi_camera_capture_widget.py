import logging
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QGridLayout

from skelly_viewer.utils.workers.video_processing_worker import VideoProcessingWorker

logger = logging.getLogger(__name__)

class MultiVideoDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.video_folder_load_button = QPushButton('Load a folder of videos', self)
        self.video_folder_load_button.setEnabled(False)
        self._layout.addWidget(self.video_folder_load_button)
        self.video_folder_load_button.clicked.connect(self.open_video_folder_dialogue)

        self.video_display_layout = QGridLayout()
        self._layout.addLayout(self.video_display_layout)

        self.are_videos_loaded = False  # bool to let you move the slider in the main GUI without having loaded videos

    def set_session_folder_path(self, session_folder_path: Path):
        self.session_folder_path = session_folder_path

    def open_video_folder_dialogue(self):
        self.folder_diag = QFileDialog()
        self.video_folder_path = QFileDialog.getExistingDirectory(None, "Choose a folder of videos",
                                                                  directory=str(self.session_folder_path))
        self.load_video_folder_from_path(self.video_folder_path)

    def load_video_folder_from_path(self, video_folder_path: Path):
        # get a path to the video folder, generate a list of the video paths and the number of videos and create the video display widget based on that
        self.video_folder_path = video_folder_path
        # self.folder_diag = QFileDialog()
        # self.video_folder_path = QFileDialog.getExistingDirectory(None, "Choose a folder of videos",
        #                                                          directory=str(self.session_folder_path))
        self.list_of_video_paths, self.number_of_videos = self.create_list_of_video_paths(self.video_folder_path)
        self.generate_video_display(self.list_of_video_paths, self.number_of_videos)

        self.are_videos_loaded = True

    def create_list_of_video_paths(self, path_to_video_folder: Path):
        # search the folder for 'mp4' files and create a list of them
        list_of_video_paths = list(Path(path_to_video_folder).glob('*.mp4'))
        number_of_videos = len(list_of_video_paths)
        return list_of_video_paths, number_of_videos

    def generate_video_display(self, list_of_video_paths: list, number_of_videos: int):
        self.video_worker_dictionary = self.generate_video_workers(list_of_video_paths)
        self.video_frame_label_widget_dictionary = self.generate_label_widgets_for_videos(number_of_videos)
        self.add_widgets_to_layout()

        return self.video_worker_dictionary, self.video_frame_label_widget_dictionary

    def generate_video_workers(self, list_of_video_paths: list):
        # for every video, create a worker that can handle the video processing and add it to the dictionary
        self.video_worker_dictionary = {}

        for count, video_path in enumerate(list_of_video_paths):
            self.video_worker_dictionary[count] = VideoProcessingWorker(video_path)

        return self.video_worker_dictionary
        f = 2

    def generate_label_widgets_for_videos(self, number_of_videos: int):
        label_widget_dictionary = {}
        for x in range(number_of_videos):
            label_widget_dictionary[x] = QLabel('Video {}'.format(str(x)))

        self.number_of_videos = number_of_videos

        return label_widget_dictionary

    def add_widgets_to_layout(self):
        column_count = 0
        row_count = 0
        for widget in self.video_frame_label_widget_dictionary:
            self.video_display_layout.addWidget(self.video_frame_label_widget_dictionary[widget], row_count, column_count)

            # This section is for formatting the videos in the grid nicely - it fills out two columns and then moves on to the next row
            column_count += 1
            if column_count % 2 == 0:
                column_count = 0
                row_count += 1

    def update_display(self, frame_number: int):
        logger.debug(f"Updating video display to frame#{frame_number}")
        for video_worker, video_frame_label_widget in zip(self.video_worker_dictionary.values(),
                                                          self.video_frame_label_widget_dictionary.values()):
            video_worker.increment_frame_number(frame_number)
            video_frame_label_widget.setPixmap(video_worker.pixmap)
