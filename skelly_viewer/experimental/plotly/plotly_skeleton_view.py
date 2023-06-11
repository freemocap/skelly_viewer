import json
import logging
from pathlib import Path
from typing import Union

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Dash, Output, Input

# Silence the werkzeug logger
logging.getLogger('werkzeug').setLevel(logging.WARNING)

class DataLoader:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)

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


class FrameCreator:
    @staticmethod
    def create_frame(frame_number, frame_data):
        body = frame_data["body"]
        body_names = list(body.keys())
        return go.Frame(
            data=[
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
    @staticmethod
    def create_frames(data_by_frame):
        frames = []
        for frame_number, frame_data in data_by_frame.items():
            frames.append(FrameCreator.create_frame(frame_number, frame_data))
        return frames


class FigureCreator:
    def __init__(self, axis_props, ax_range, updatemenus):
        self.axis_props = axis_props
        self.ax_range = ax_range
        self.updatemenus = updatemenus

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
                updatemenus=self.updatemenus
            ),
            frames=frames
        )

        return fig


class DashAppCreator:
    @staticmethod
    def create_dash_app(figure):
        app = Dash(__name__)
        app.layout = html.Div([
            dcc.Graph(id='animation-graph', figure=figure, style={'height': '100%', 'width': '100%'})
        ], style={'height': '100%', 'width': '100%'})

        return app


class WidgetManager:
    @staticmethod
    def add_button(layout, label, method, args):
        layout.append(dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label=label,
                method=method,
                args=args
            )]
        ))

    @staticmethod
    def add_slider(layout, min_value, max_value, value, step):
        layout.append(dcc.Slider(
            min=min_value,
            max=max_value,
            value=value,
            step=step
        ))

    @staticmethod
    def add_widgets(layout):
        WidgetManager.add_button(layout, 'Play', 'animate', [None, {"frame": {"duration": 30}}])
        # You can add more buttons, sliders, etc here.

class SkeletonViewer:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)
        self.ax_range = 5000
        self.axis_props = dict(
            showbackground=True,
            backgroundcolor="rgb(230, 230,230)",
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
        )
        self.data_loader = DataLoader(self.recording_folder_path)

    def create_app(self):
        data_by_frame = self.data_loader.load_data_by_frame()
        self.frames = FrameCreator.create_frames(data_by_frame)

        updatemenus = []
        WidgetManager.add_widgets(updatemenus)

        figure_creator = FigureCreator(self.axis_props, self.ax_range, updatemenus)
        fig = figure_creator.create_figure(self.frames)

        app = DashAppCreator.create_dash_app(fig)

        app.layout.children.append(
            dcc.Slider(
                id='frame-slider',
                min=0,
                max=len(self.frames) - 1,
                value=0,
                step=1,
                marks={i: str(i) for i in range(len(self.frames))},
            )
        )

        @app.callback(
            Output('animation-graph', 'figure'),
            [Input('frame-slider', 'value')])
        def update_figure(selected_frame):
            new_figure = go.Figure(data=self.frames[selected_frame]['data'])
            new_figure.update_layout(fig.layout)
            new_figure['layout']['scene']['camera']['eye'] = fig['layout']['scene']['camera']['eye']
            new_figure.layout.updatemenus[0].buttons[0].args[1]['frame']['name'] = self.frames[selected_frame][
                'name']  # Update the frame
            return new_figure

        return app

if __name__ == "__main__":
    recording_folder_path = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    viewer = SkeletonViewer(recording_folder_path)
    app = viewer.create_app()
    app.run_server(debug=True)
