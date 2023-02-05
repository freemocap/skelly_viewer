from pathlib import Path

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMainWindow, QHBoxLayout

from skelly_viewer import SkellyViewer
from skelly_viewer.config.folder_directory import MEDIAPIPE_3D_BODY_FILE_NAME, DATA_FOLDER_NAME


class SkellyViewerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Skelly Viewer \U0001F480 \U0001F440')
        self.setGeometry(100, 100, 1200, 600)
        widget = QWidget()
        self._layout = QVBoxLayout()
        widget.setLayout(self._layout)
        self.setCentralWidget(widget)

        self._folder_open_button = QPushButton('Load a session folder', self)
        self._folder_open_button.clicked.connect(self._open_session_folder_dialog)

        # self._video_folder_load_button = QPushButton('Load a folder of videos', self)
        # self._video_folder_load_button.setEnabled(False)
        # self._video_folder_load_button.clicked.connect(self.open_video_folder_dialogue)

        hbox = QHBoxLayout()
        hbox.addWidget(self._folder_open_button)
        # hbox.addWidget(self._video_folder_load_button)
        self._layout.addLayout(hbox)


        self._skelly_viewer = SkellyViewer()
        self._layout.addWidget(self._skelly_viewer)

    def _open_session_folder_dialog(self):
        self._session_folder_path = QFileDialog.getExistingDirectory(None, "Choose a session")

        if self._session_folder_path:
            self._session_folder_path = Path(self._session_folder_path)
            self._skelly_viewer.set_data_paths(
                mediapipe_skeleton_npy_path=self._session_folder_path / DATA_FOLDER_NAME / MEDIAPIPE_3D_BODY_FILE_NAME,
                video_folder_path=self._try_to_find_synchronized_videos_folder_path(self._session_folder_path)
            )

    # def open_video_folder_dialogue(self):
    #     self.folder_diag = QFileDialog()
    #     self.video_folder_path = QFileDialog.getExistingDirectory(None, "Choose a folder of videos",
    #                                                               directory=str(self.session_folder_path))
    #     self.load_video_folder_from_path(self.video_folder_path)

    def _try_to_find_synchronized_videos_folder_path(self, session_folder_path: Path) -> Path:
        for subfolder_path in session_folder_path.iterdir():
            if subfolder_path.name == 'annotated_videos':
                return subfolder_path
            if subfolder_path.name == 'synchronized_videos':
                return subfolder_path
            if subfolder_path.name == 'SyncedVideos':
                return subfolder_path

        return

def main():
    app = QApplication([])
    win = SkellyViewerMainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
