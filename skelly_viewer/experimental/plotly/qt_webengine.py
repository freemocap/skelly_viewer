import sys
import threading

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow, QApplication

from skelly_viewer.experimental.plotly.plotly_skeleton_view import SkeletonViewer


class ViewerApp(QMainWindow):
    def __init__(self, dash_app, parent=None):
        super(ViewerApp, self).__init__(parent)
        self.setWindowTitle("Skeleton Viewer App")

        # Set QWebEngineView as the central widget
        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://localhost:8050"))
        self.setCentralWidget(self.browser)

        # Run the Dash app in a separate thread
        threading.Thread(target=dash_app.run_server, kwargs={'port': 8050}).start()


if __name__ == "__main__":
    recording_folder_path = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    viewer = SkeletonViewer(recording_folder_path)
    dash_app = viewer.create_app()

    # Create a PyQt application
    app = QApplication(sys.argv)

    # Initialize our ViewerApp
    viewer_app = ViewerApp(dash_app)

    # Show and execute the application
    viewer_app.show()
    sys.exit(app.exec())
