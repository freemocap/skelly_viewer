
import matplotlib
from PySide6.QtWidgets import QWidget, QVBoxLayout

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from skelly_viewer.utilities.mediapipe_skeleton_builder import mediapipe_indices


import numpy as np

class TimeSeriesPlotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=15, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.x_ax = fig.add_subplot(311)
        self.y_ax = fig.add_subplot(312)
        self.z_ax = fig.add_subplot(313)

        super(TimeSeriesPlotCanvas, self).__init__(fig)

class TimeSeriesPlotterWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.fig, self.axes_list = self.initialize_skeleton_plot()

        toolbar = NavigationToolbar(self.fig, self)

        self._layout.addWidget(toolbar)
        self._layout.addWidget(self.fig)

    def initialize_skeleton_plot(self):
        fig = TimeSeriesPlotCanvas(self, width=15, height=10, dpi=100)
        self.x_ax = fig.figure.axes[0]
        self.y_ax = fig.figure.axes[1]
        self.z_ax = fig.figure.axes[2]

        self.axes_list = [self.x_ax,self.y_ax,self.z_ax]
        return fig, self.axes_list

    def get_mediapipe_indices(self,marker_to_plot):
        mediapipe_index = mediapipe_indices.index(marker_to_plot)
        return mediapipe_index
    

    def update_plot(self,marker_to_plot:str, freemocap_data:np.ndarray):
        mediapipe_index = self.get_mediapipe_indices(marker_to_plot)

        axes_names = ['X Axis', 'Y Axis', 'Z Axis']

        for dimension, (ax,ax_name) in enumerate(zip(self.axes_list,axes_names)):

            ax.cla()
            ax.plot(freemocap_data[:,mediapipe_index,dimension], label = 'FreeMoCap', alpha = .7)

            ax.set_ylabel(ax_name)
            
            if dimension == 2: #put the xlabel only on the last plot
                ax.set_xlabel('Frame #')

            ax.legend()

        self.fig.figure.canvas.draw_idle()
