import numpy as np
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout

from skelly_viewer.gui.qt.widgets.time_series_widgets.sub_widgets.marker_selector_widget import MarkerSelectorWidget
from skelly_viewer.gui.qt.widgets.time_series_widgets.trajectory_view_widget import TimeSeriesPlotterWidget


class TimeSeriesViewer(QWidget):
    def __init__(self, freemocap_data:np.ndarray):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.freemocap_data = freemocap_data

        self.marker_selector_widget = MarkerSelectorWidget()
        self.layout.addWidget(self.marker_selector_widget)

        self.time_series_plotter_widget = TimeSeriesPlotterWidget()
        self.layout.addWidget(self.time_series_plotter_widget)


        self.connect_signals_to_slots()

    def connect_signals_to_slots(self):
        self.marker_selector_widget.marker_to_plot_updated_signal.connect(lambda: self.time_series_plotter_widget.update_plot(self.marker_selector_widget.current_marker,self.freemocap_data))


if __name__ == "__main__":
    
    class MainWindow(QMainWindow):
        def __init__(self, freemocap_data:np.ndarray):
            super().__init__()
        
            layout = QVBoxLayout()
            widget = QWidget()

            self.time_series_viewer = TimeSeriesViewer(freemocap_data)
            layout.addWidget(self.time_series_viewer)

            widget.setLayout(layout)
            self.setCentralWidget(widget)


    path_to_mediapipe_npy_file = r"C:\Users\jonma\freemocap_data\recording_sessions\session_2023-02-15_08_46_43_wud\recording_08_47_25_gmt-5_wud\output_data\raw_data\mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy"
    freemocap_data = np.load(path_to_mediapipe_npy_file)

    app = QApplication([])
    win = MainWindow(freemocap_data)
    win.show()
    app.exec()
