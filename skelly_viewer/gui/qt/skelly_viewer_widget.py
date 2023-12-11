from pathlib import Path
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from skelly_viewer.gui.qt.widgets.multi_video_display import MultiVideoDisplay
from skelly_viewer.gui.qt.widgets.skeleton_view_widget import SkeletonViewWidget
from skelly_viewer.gui.qt.widgets.slider_widget import PlayPauseCountSlider


class SkellyViewer(QWidget):
    # session_folder_loaded_signal = Signal()
    def __init__(self, mediapipe_skeleton_npy_path=None, video_folder_path=None):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        skeleton_and_videos_layout = QHBoxLayout()
        skeleton_and_videos_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._skeleton_view_widget = SkeletonViewWidget()
        self._skeleton_view_widget.setFixedSize(self._skeleton_view_widget.size())
        skeleton_and_videos_layout.addWidget(self._skeleton_view_widget)
        layout.addLayout(skeleton_and_videos_layout)

        self.multi_video_display = MultiVideoDisplay()
        # self.multi_video_display.setFixedSize(self.skeleton_view_widget.size()*1.5)
        skeleton_and_videos_layout.addWidget(self.multi_video_display)

        self._frame_count_slider = PlayPauseCountSlider()
        self._frame_count_slider.setEnabled(False)
        layout.addWidget(self._frame_count_slider)

        self.connect_signals_to_slots()

        self._is_video_display_enabled = True

        if mediapipe_skeleton_npy_path is not None:
            self.load_skeleton_data(mediapipe_skeleton_npy_path)

        if video_folder_path is not None:
            self.generate_video_display(video_folder_path)

    def load_skeleton_data(self, mediapipe_skeleton_npy_path: Union[str, Path]):
        self._skeleton_view_widget.load_skeleton_data(mediapipe_skeleton_npy_path)

    def generate_video_display(self, video_folder_path: Union[str, Path]):
        self.multi_video_display.generate_video_display(video_folder_path)
        self.multi_video_display.update_display(self._frame_count_slider._slider.value())

    def set_data_paths(self,
                       mediapipe_skeleton_npy_path: Union[str, Path],
                       video_folder_path: Union[str, Path]):

        self.load_skeleton_data(mediapipe_skeleton_npy_path)
        self.generate_video_display(video_folder_path)

        self._frame_count_slider._slider.setValue(0)

    def connect_signals_to_slots(self):
        self._skeleton_view_widget.skeleton_data_loaded_signal.connect(
            self._handle_data_loaded_signal)

        self._frame_count_slider._slider.valueChanged.connect(self._handle_slider_value_changed)

    def _handle_data_loaded_signal(self):
        self._frame_count_slider.set_slider_range(self._skeleton_view_widget._number_of_frames)
        self._frame_count_slider.setEnabled(True)

    def _handle_slider_value_changed(self):
        self._skeleton_view_widget.update_skeleton_plot(self._frame_count_slider._slider.value())
        if self._is_video_display_enabled:
            self.multi_video_display.update_display(self._frame_count_slider._slider.value())

    def toggle_video_display(self):
        self._is_video_display_enabled = not self._is_video_display_enabled
        self.multi_video_display.setVisible(self._is_video_display_enabled)
