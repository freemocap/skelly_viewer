

from pathlib import Path

import numpy as np

from skelly_viewer.config.folder_directory import MEDIAPIPE_3D_BODY_FILE_NAME, DATA_FOLDER_NAME, \
    TOTAL_BODY_CENTER_OF_MASS_NPY_FILE_NAME


class FreeMoCapDataLoader():
    def __init__(self, path_to_session_folder:Path):
        self.path_to_session_folder = path_to_session_folder

    def load_mediapipe_body_data(self):
        self.path_to_mediapipe_body_data = self.path_to_session_folder/DATA_FOLDER_NAME/MEDIAPIPE_3D_BODY_FILE_NAME
        mediapipe_body_data = np.load(self.path_to_mediapipe_body_data)
        return mediapipe_body_data

    def load_total_body_COM_data(self):
        self.path_to_total_body_COM_data = self.path_to_session_folder/DATA_FOLDER_NAME/TOTAL_BODY_CENTER_OF_MASS_NPY_FILE_NAME
        total_body_COM_data = np.load(self.path_to_total_body_COM_data)
        return total_body_COM_data




