from pathlib import Path
from typing import Union

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMainWindow, QHBoxLayout

from skelly_viewer import SkellyViewer
from skelly_viewer.utilities.freemocap_data_loader import FreeMoCapDataLoader


class SkellyViewerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Skelly Viewer \U0001F480 \U0001F440')
        self.setGeometry(100, 100, 1200, 600)
        widget = QWidget()
        self._layout = QVBoxLayout()
        widget.setLayout(self._layout)
        self.setCentralWidget(widget)

        hbox = QHBoxLayout()
        self._layout.addLayout(hbox)

        self._folder_open_button = QPushButton('Load a session folder', self)
        self._folder_open_button.clicked.connect(self._open_session_folder_dialog)
        hbox.addWidget(self._folder_open_button)

        # self._sample_data_loader_button = QPushButton('Load sample data', self)
        # self._sample_data_loader_button.clicked.connect(lambda: self._load_data(path=load_sample_data()))
        # hbox.addWidget(self._sample_data_loader_button)

        self._toggle_video_display_button = QPushButton('Toggle Video Display', self)
        self._toggle_video_display_button.clicked.connect(self._toggle_video_display)
        hbox.addWidget(self._toggle_video_display_button)

        self._skelly_viewer = SkellyViewer()
        self._layout.addWidget(self._skelly_viewer)

    def _toggle_video_display(self):
        self._skelly_viewer.toggle_video_display()
        
    def _open_session_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Choose a FreeMoCap recording folder",)

        if folder_path:
            self._load_data(path=folder_path)

    # def open_video_folder_dialogue(self):
    #     self.folder_diag = QFileDialog()
    #     self.video_folder_path = QFileDialog.getExistingDirectory(None, "Choose a folder of videos",
    #                                                               directory=str(self.session_folder_path))
    #     self.load_video_folder_from_path(self.video_folder_path)

    def _load_data(self, path: Union[Path, str]):
        self._session_folder_path = Path(path)
        data_loader = FreeMoCapDataLoader(path_to_session_folder=self._session_folder_path)

        self._skelly_viewer.set_data_paths(
            mediapipe_skeleton_npy_path=data_loader.find_skeleton_npy_file_name(),
            video_folder_path=data_loader.find_synchronized_videos_folder_path()
        )


def main():
    app = QApplication([])
    win = SkellyViewerMainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
