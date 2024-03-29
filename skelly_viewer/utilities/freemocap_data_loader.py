from pathlib import Path

import numpy as np

from skelly_viewer.config.folder_and_file_names import MEDIAPIPE_3D_BODY_FILE_NAME, OUTPUT_DATA_FOLDER_NAME, \
    TOTAL_BODY_CENTER_OF_MASS_NPY_FILE_NAME


class FreeMoCapDataLoader:
    def __init__(self, path_to_session_folder: Path):
        self._recording_folder_path = path_to_session_folder

    def load_mediapipe_body_data(self):
        path_to_mediapipe_body_data = self.find_output_data_folder_path()
        mediapipe_body_data = np.load(str(path_to_mediapipe_body_data))
        return mediapipe_body_data

    def load_total_body_COM_data(self):
        path_to_total_body_COM_data = self.find_output_data_folder_path() / TOTAL_BODY_CENTER_OF_MASS_NPY_FILE_NAME
        total_body_COM_data = np.load(str(path_to_total_body_COM_data))
        return total_body_COM_data

    def find_output_data_folder_path(self, ) -> Path:
        for subfolder_path in self._recording_folder_path.iterdir():
            if subfolder_path.name == OUTPUT_DATA_FOLDER_NAME:
                return subfolder_path
            if subfolder_path.name == 'DataArrays':
                return subfolder_path

        raise Exception(f"Could not find a data folder in path {str(self._recording_folder_path)}")

    def find_skeleton_npy_file_name(self) -> Path:

        npy_path_list = [path.name for path in self.find_output_data_folder_path().glob("*.npy")]

        if 'mediaPipeSkel_3d_origin_aligned.npy' in npy_path_list:
            return self.find_output_data_folder_path() / MEDIAPIPE_3D_BODY_FILE_NAME

        if 'mediapipe_body_3d_xyz.npy' in npy_path_list:
            return self.find_output_data_folder_path() / 'mediapipe_body_3d_xyz.npy'

        raise Exception(f"Could not find a skeleton NPY file in path {str(self.find_output_data_folder_path())}")

    def find_synchronized_videos_folder_path(self) -> Path:
        subpaths = list(self._recording_folder_path.glob('*'))

        if self._recording_folder_path / 'annotated_videos' in subpaths:
            return self._recording_folder_path / 'annotated_videos'
        if self._recording_folder_path / 'synchronized_videos' in subpaths:
            return self._recording_folder_path / 'synchronized_videos'
        if self._recording_folder_path / 'SyncedVideos' in subpaths:
            return self._recording_folder_path / 'SyncedVideos'

        raise Exception(f"Could not find a videos folder in path {str(self._recording_folder_path)}")
