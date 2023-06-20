import sys
import threading

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

from skelly_viewer.experimental.plotly_exp.capture_volume_3d_viewer import CaptureVolume3dViewer


class View3dWidget(QWidget):
    def __init__(self, dash_app, parent=None):
        super(View3dWidget, self).__init__(parent)
        self.setWindowTitle("Skeleton Viewer App")

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://localhost:8050"))
        self._layout.addWidget(self.browser)

        # Run the Dash app in a separate thread
        self._thread = threading.Thread(target=dash_app.run_server, kwargs={'port': 8050}).start()

    def closeEvent(self, event):
        self.browser.close()
        self.browser.deleteLater()
        super(View3dWidget, self).closeEvent(event)
        self._thread.terminate()



if __name__ == "__main__":
    recording_folder_path = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    viewer = CaptureVolume3dViewer(recording_folder_path)
    dash_app = viewer.create_app()

    # Create a PyQt application
    app = QApplication(sys.argv)

    # Initialize our ViewerApp
    viewer_app = View3dWidget(dash_app)

    # Show and execute the application
    viewer_app.show()
    sys.exit(app.exec())
