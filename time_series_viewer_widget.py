
from pathlib import Path
import numpy as np

from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout,QVBoxLayout

from time_series_widgets.trajectory_view_widget import TimeSeriesPlotterWidget
from time_series_widgets.marker_selector_widget import MarkerSelectorWidget

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


    path_to_freemocap_session_folder = Path(r'D:\ValidationStudy2022\FreeMocap_Data\sesh_2022-05-24_15_55_40_JSM_T1_BOS')
    freemocap_data = np.load(path_to_freemocap_session_folder/'DataArrays'/'mediaPipeSkel_3d_origin_aligned.npy')

    app = QApplication([])
    win = MainWindow(freemocap_data)
    win.show()
    app.exec()
