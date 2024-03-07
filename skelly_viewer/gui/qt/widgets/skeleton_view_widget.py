from typing import Union

import matplotlib
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from skelly_viewer.utilities.mediapipe_skeleton_builder import build_skeleton, mediapipe_indices, mediapipe_connections

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pathlib import Path
import numpy as np

class SkeletonViewWidget(QWidget):
    skeleton_data_loaded_signal = Signal()

    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._figure_widget, self._3d_axes = self.initialize_skeleton_plot()
        self._layout.addWidget(self._figure_widget)
        self._skel_bones = None

    def load_skeleton_data(self, mediapipe_skeleton_npy_path: Union[str, Path]):
        self._skeleton_3d_frame_marker_xyz = np.load(str(mediapipe_skeleton_npy_path))
        self._mediapipe_skeleton = build_skeleton(skeleton_3d_frame_marker_xyz=self._skeleton_3d_frame_marker_xyz,
                                                  pose_estimation_markers_list=mediapipe_indices,
                                                  pose_estimation_connections_dict=mediapipe_connections)

        self._number_of_frames = self._skeleton_3d_frame_marker_xyz.shape[0]
        self._initialize_3d_axes()

        self.skeleton_data_loaded_signal.emit()

    def initialize_skeleton_plot(self):
        figure_widget = Mpl3DPlotCanvas(parent=self)
        figure_widget.setMinimumSize(100, 100)
        axes = figure_widget.figure.axes[0]
        return figure_widget, axes

    def _initialize_3d_axes(self):
        self._3d_axes.cla()
        self._calculate_axes_means(self._skeleton_3d_frame_marker_xyz)
        self.skel_x, self.skel_y, self.skel_z = self._get_x_y_z_data(0)
        self.skel_points = self._3d_axes.scatter(self.skel_x, self.skel_y, self.skel_z, 'ko', s=1)
        self._skel_bones = None
        self.skel_bones = self._plot_skeleton_bones(0)

    def reset_slider(self):
        self._slider_max = self._number_of_frames - 1
        self.slider.setValue(0)
        self.slider.setMaximum(self._slider_max)

    def _calculate_axes_means(self, skeleton_3d_frame_marker_xyz: np.ndarray):
        self._data_midpoint_x = np.nanmean(skeleton_3d_frame_marker_xyz[:, :, 0])
        self._data_midpoint_y = np.nanmean(skeleton_3d_frame_marker_xyz[:, :, 1])
        self._data_midpoint_z = np.nanmean(skeleton_3d_frame_marker_xyz[:, :, 2])
        self._axes_3d_range = 1000

    def _plot_skeleton(self, frame_number, skeleton_points_x, skeleton_points_y, skeleton_points_z):
        
        self.skel_points.set_offsets(np.column_stack([skeleton_points_x, skeleton_points_y]))
        self.skel_points.set_3d_properties(skeleton_points_z, zdir='z')
        self._plot_skeleton_bones(frame_number)

        self._3d_axes.set_xlim(
        [self._data_midpoint_x - self._axes_3d_range, self._data_midpoint_x + self._axes_3d_range])
        self._3d_axes.set_ylim(
        [self._data_midpoint_y - self._axes_3d_range, self._data_midpoint_y + self._axes_3d_range])
        self._3d_axes.set_zlim(
        [self._data_midpoint_z - self._axes_3d_range, self._data_midpoint_z + self._axes_3d_range])

        self._figure_widget.figure.canvas.draw_idle()

    def _plot_skeleton_bones(self, frame_number):
        if self._skel_bones is None:
            this_frame_skeleton_data = self._mediapipe_skeleton[frame_number]
            self._skel_bones = []
            for connection in this_frame_skeleton_data.keys():
                line_start_point = this_frame_skeleton_data[connection][0]
                line_end_point = this_frame_skeleton_data[connection][1]

                bone_x, bone_y, bone_z = [line_start_point[0], line_end_point[0]], [line_start_point[1],
                                                                                    line_end_point[1]], [
                                             line_start_point[2], line_end_point[2]]
                bone = self._3d_axes.plot(bone_x, bone_y, bone_z)[0]
                self._skel_bones.append(bone)
        else:
            this_frame_skeleton_data = self._mediapipe_skeleton[frame_number]
            for i, connection in enumerate(this_frame_skeleton_data.keys()):
                line_start_point = this_frame_skeleton_data[connection][0]
                line_end_point = this_frame_skeleton_data[connection][1]

                bone_x, bone_y, bone_z = [line_start_point[0], line_end_point[0]], [line_start_point[1],
                                                                                    line_end_point[1]], [
                                             line_start_point[2], line_end_point[2]]
                bone = self._skel_bones[i]
                bone.set_xdata(bone_x)
                bone.set_ydata(bone_y)
                bone.set_3d_properties(bone_z)


    def _get_x_y_z_data(self, frame_number: int):
        
        skel_x = self._skeleton_3d_frame_marker_xyz[frame_number, :, 0]
        skel_y = self._skeleton_3d_frame_marker_xyz[frame_number, :, 1]
        skel_z = self._skeleton_3d_frame_marker_xyz[frame_number, :, 2]

        return skel_x, skel_y, skel_z

    def update_skeleton_plot(self, frame_number: int):
        skel_x, skel_y, skel_z = self._get_x_y_z_data(frame_number)
        self.skel_points.set_offsets(np.column_stack([skel_x, skel_y]))
        self.skel_points.set_3d_properties(skel_z, zdir='z')
        self._plot_skeleton_bones(frame_number)
        self._3d_axes.set_xlim(
            [self._data_midpoint_x - self._axes_3d_range, self._data_midpoint_x + self._axes_3d_range])
        self._3d_axes.set_ylim(
            [self._data_midpoint_y - self._axes_3d_range, self._data_midpoint_y + self._axes_3d_range])
        self._3d_axes.set_zlim(
            [self._data_midpoint_z - self._axes_3d_range, self._data_midpoint_z + self._axes_3d_range])
        self._figure_widget.figure.canvas.draw_idle()

class Mpl3DPlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super(Mpl3DPlotCanvas, self).__init__(fig)
