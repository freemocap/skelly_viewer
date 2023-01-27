from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout

from utils.GUI_widgets.skeleton_view_widget import SkeletonViewWidget
from utils.GUI_widgets.slider_widget import FrameCountSlider
from utils.GUI_widgets.multi_camera_capture_widget import MultiVideoDisplay

from pathlib import Path


class SkellyViewer(QWidget):
    # session_folder_loaded_signal = pyqtSignal()
    def __init__(self, path_to_session_folder=None, path_to_video_folder=None):
        super().__init__()

        layout = QHBoxLayout()

        slider_and_skeleton_layout = QVBoxLayout()

        self.frame_count_slider = FrameCountSlider()
        slider_and_skeleton_layout.addWidget(self.frame_count_slider)

        self.skeleton_view_widget = SkeletonViewWidget()
        self.skeleton_view_widget.setFixedSize(self.skeleton_view_widget.size())
        slider_and_skeleton_layout.addWidget(self.skeleton_view_widget)
        layout.addLayout(slider_and_skeleton_layout)

        self.multi_video_display = MultiVideoDisplay()
        # self.multi_video_display.setFixedSize(self.skeleton_view_widget.size()*1.5)
        layout.addWidget(self.multi_video_display)

        self.setLayout(layout)

        self.connect_signals_to_slots()

        if path_to_session_folder and path_to_video_folder:
            # this block of code disables the buttons and lets you specify session and video paths in the widget call
            self.path_to_session_folder = path_to_session_folder
            self.path_to_video_folder = path_to_video_folder
            self.skeleton_view_widget.load_session_data(self.path_to_session_folder)
            self.multi_video_display.load_video_folder_from_path(self.path_to_video_folder)

            self.multi_video_display.video_folder_load_button.setEnabled(False)
            self.skeleton_view_widget.folder_open_button.setEnabled(False)
        f = 2

    def connect_signals_to_slots(self):
        self.skeleton_view_widget.session_folder_loaded_signal.connect(
            lambda: self.frame_count_slider.set_slider_range(self.skeleton_view_widget.num_frames))
        self.skeleton_view_widget.session_folder_loaded_signal.connect(
            lambda: self.multi_video_display.video_folder_load_button.setEnabled(True))
        self.skeleton_view_widget.session_folder_loaded_signal.connect(
            lambda: self.multi_video_display.set_session_folder_path(self.skeleton_view_widget.session_folder_path))

        self.frame_count_slider.slider.valueChanged.connect(
            lambda: self.skeleton_view_widget.replot(self.frame_count_slider.slider.value()))
        self.frame_count_slider.slider.valueChanged.connect(
            lambda: self.multi_video_display.update_display(self.frame_count_slider.slider.value()) if (
                self.multi_video_display.are_videos_loaded) else None)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        path_to_session = None
        path_to_videos = None

        self.skelly_viewer = SkellyViewer(path_to_session, path_to_videos)
        self.setCentralWidget(self.skelly_viewer)


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
