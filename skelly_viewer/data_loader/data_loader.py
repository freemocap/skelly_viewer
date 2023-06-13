import json
from pathlib import Path
from typing import Union

import pandas as pd


class DataLoader:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)
        self.data_by_trajectory = self.load_data_by_trajectory()
        self.data_by_frame = self.load_data_by_frame()

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


    def get_trajectory(self, trajectory_name):
        return self.data_by_trajectory.loc[self.data_by_trajectory["trajectory_name"] == trajectory_name]
