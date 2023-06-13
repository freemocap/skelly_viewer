import json
from pathlib import Path
from typing import Union

import pandas as pd


class DataLoader:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)
        self.data_by_trajectory = self.load_data_by_trajectory()
        self.data_by_frame = self.load_data_by_frame()
        self._frame_number = -1

    def load_data_by_trajectory(self):
        file_name = f"{self.recording_folder_path.name}_by_trajectory.csv"
        file_path = self.recording_folder_path / file_name
        return pd.read_csv(file_path)

    def load_data_by_frame(self):
        file_name = f"{self.recording_folder_path.name}_by_frame.json"
        file_path = self.recording_folder_path / file_name

        with open(file_path, "r") as f:
            data = json.load(f)
        return data["data_by_frame"]

    def get_frame_data(self, frame_number: Union[int, str] = None):
        if frame_number is None:
            self._frame_number += 1
        else:
            self._frame_number = frame_number

        self._frame_number = self._frame_number % len(self.data_by_frame)
        return self.data_by_frame[str(self._frame_number)]

    def get_trajectory(self, trajectory_name):
        return self.data_by_trajectory.loc[self.data_by_trajectory["trajectory_name"] == trajectory_name]
