import json
from pathlib import Path
from typing import Union

import pandas as pd
import plotly.graph_objects as go
from dash import Dash
from dash import dcc, html


class SkeletonViewer:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)
        self.data_by_frame = self.load_data_by_frame()
        self.data_by_trajectory = self.load_data_by_trajectory()
        self.ax_range = 5000
        self.axis_props = dict(
            showbackground=True,
            backgroundcolor="rgb(230, 230,230)",
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
        )

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

    def create_frames(self):
        frames = []
        for frame_number, frame_data in self.data_by_frame.items():
            frames.append(self.create_frame(frame_number, frame_data))
        return frames

    def create_frame(self, frame_number, frame_data):
        center_of_mass = frame_data["center_of_mass"]["full_body_com"]
        body = frame_data["body"]
        body_names = list(body.keys())
        return go.Frame(data=[
            go.Scatter3d(
                x=[point["x"] for point in body.values()],
                y=[point["y"] for point in body.values()],
                z=[point["z"] for point in body.values()],
                mode='markers',
                marker=dict(
                    size=3,
                    color='purple',
                    colorscale='Viridis',  # choose a colorscale
                ),
                ids=body_names,

            )
        ],
            name=str(frame_number)
        )

    def create_figure(self, frames):
        fig = go.Figure(
            data=[frames[0]['data'][0]],
            layout=go.Layout(
                scene=dict(
                    xaxis=dict(self.axis_props, range=[-self.ax_range, self.ax_range]),
                    yaxis=dict(self.axis_props, range=[-self.ax_range, self.ax_range]),
                    zaxis=dict(self.axis_props, range=[-self.ax_range, self.ax_range]),
                    aspectmode='cube'
                ),
                updatemenus=[dict(
                    type='buttons',
                    showactive=False,
                    buttons=[dict(
                        label='Play',
                        method='animate',
                        args=[None, {"frame": {"duration": 30}}]
                    )]
                )]
            ),
            frames=frames
        )

        return fig

    def create_dash_app(self):
        frames = self.create_frames()
        fig = self.create_figure(frames)

        app = Dash(__name__)
        app.layout = html.Div([
            dcc.Graph(figure=fig)
        ])

        return app


if __name__ == "__main__":
    recording_folder_path = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    viewer = SkeletonViewer(recording_folder_path)
    app = viewer.create_dash_app()
    app.run_server(debug=True)
