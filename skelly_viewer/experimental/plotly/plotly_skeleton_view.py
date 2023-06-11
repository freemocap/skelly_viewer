import json
from pathlib import Path
from typing import Union, Dict

import numpy as np
import plotly.graph_objects as go


def calculate_axes_means(skeleton_3d_data):
    mx_skel = np.nanmean(skeleton_3d_data[:, 0:33, 0])
    my_skel = np.nanmean(skeleton_3d_data[:, 0:33, 1])
    mz_skel = np.nanmean(skeleton_3d_data[:, 0:33, 2])

    return mx_skel, my_skel, mz_skel


def load_data_by_frame(recording_folder_path: Union[str, Path]):
    rec_path = Path(recording_folder_path)
    file_name = f"{rec_path.name}_by_frame.json"
    file_path = rec_path / file_name

    with open(file_path, "r") as f:
        data = json.load(f)
    return data["data_by_frame"]


def plotly_skeleton_view(data_by_frame: Dict[str, Dict[str, np.ndarray]]):
    ax_range = 5000

    mx_skel = 0
    my_skel = 0
    mz_skel = 0

    frames = []
    for frame_number, frame_data in data_by_frame.items():
        body = frame_data["body"]
        x_data = [point["x"] for point in body.values()]
        y_data = [point["y"] for point in body.values()]
        z_data = [point["z"] for point in body.values()]



        frames.append(go.Frame(data=[
            go.Scatter3d(
                x=x_data,
                y=y_data,
                z=z_data,
                mode='markers',
                marker=dict(
                    size=2,  # Adjust marker size as needed
                )
            )
        ],
            name=str(frame_number)
        )
        )

    # Define axis properties
    axis = dict(
        showbackground=True,
        backgroundcolor="rgb(230, 230,230)",
        gridcolor="rgb(255, 255, 255)",
        zerolinecolor="rgb(255, 255, 255)",
    )

    # Create a figure
    fig = go.Figure(
        data=[go.Scatter3d(
            x=x_data,
            y=y_data,
            z=z_data,
            mode='markers',
            marker=dict(
                size=2,  # Adjust marker size as needed
            )
        )],
        layout=go.Layout(
            scene=dict(
                xaxis=dict(axis, range=[mx_skel - ax_range, mx_skel + ax_range]),
                yaxis=dict(axis, range=[my_skel - ax_range, my_skel + ax_range]),
                zaxis=dict(axis, range=[mz_skel - ax_range, mz_skel + ax_range]),
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

    fig.show()

if __name__ == "__main__":
    recording_folder_path = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    data_by_frame = load_data_by_frame(recording_folder_path)
    plotly_skeleton_view(data_by_frame=data_by_frame)
