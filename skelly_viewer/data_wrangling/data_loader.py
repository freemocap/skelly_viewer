import json
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd


class DataLoader:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.video_path = None
        self.recording_folder_path = Path(recording_folder_path)
        self.output_data_path = self.recording_folder_path / "output_data"
        self.data_by_trajectory = self.load_data_by_trajectory()
        self.data_by_frame = self.load_data_by_frame()
        self.body_frame_point_xyz = self.load_body_npy()
        self.center_of_mass_xyz = self.load_center_of_mass()


    @property
    def number_of_frames(self):
        return len(self.data_by_frame["data_by_frame"])

    def load_data_by_trajectory(self):
        file_name = f"{self.recording_folder_path.name}_by_trajectory.csv"
        file_path = self.recording_folder_path / file_name
        return pd.read_csv(file_path)

    def load_data_by_frame(self):
        file_name = f"{self.recording_folder_path.name}_by_frame.json"
        file_path = self.recording_folder_path / file_name

        with open(file_path, "r") as f:
            data = json.load(f)
        return data


    def load_body_npy(self):
        body_npy_filename = "mediapipe_body_3d_xyz.npy"
        return np.load(str(self.output_data_path / body_npy_filename))

    def load_center_of_mass(self):
        return np.load(str(self.output_data_path / "center_of_mass" / "total_body_center_of_mass_xyz.npy"))

    def get_video_path(self):
        videos_path = self.recording_folder_path / "annotated_videos"

        if len(list(videos_path.glob("*.mp4"))) > 0:
            return list(videos_path.glob("*.mp4"))[0]

        raise FileNotFoundError(f"No video found in {videos_path}")
