from pathlib import Path
from typing import Union

from dash import dcc, Dash, html, Input, Output, State
from plotly import graph_objects as go

from skelly_viewer.experimental.plotly.plotly_dash_setup import DataLoader, FrameCreator

# moved constants to the top
AXIS_RANGE = 5000
FRAME_DURATION = 30
FRAME_INTERVAL = 1000/30


class AppLayoutCreator:
    def __init__(self, frames):
        self.frames = frames

    def create_layout(self):
        fig_dict = {
            "data": [self.frames[0]['data'][0]],
            "layout": self._create_layout(),
            "frames": self.frames
        }

        fig = go.Figure(fig_dict)

        layout = html.Div([
            dcc.Graph(id='animation-graph', figure=fig, style={'height': '100%', 'width': '100%'}),
            dcc.Slider(
                id='frame-slider',
                min=0,
                max=len(self.frames) - 1,
                value=0,
            ),
            dcc.Interval(
                id='frame-interval',
                interval=FRAME_INTERVAL,  # in milliseconds
                n_intervals=0
            )
        ])

        return fig, layout

    def _create_layout(self):
        axis_props = dict(
            showbackground=True,
            backgroundcolor="rgb(230, 230,230)",
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
            range=[-AXIS_RANGE, AXIS_RANGE]
        )

        layout = {
            "scene": {
                "xaxis": axis_props,
                "yaxis": axis_props,
                "zaxis": axis_props,
                "aspectmode": 'cube'
            },
            "updatemenus": self._create_updatemenus()
        }

        return layout

    def _create_updatemenus(self):
        return [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": FRAME_DURATION, "redraw": False},
                                        "fromcurrent": True, "transition": {"duration": 300,
                                                                             "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                          "mode": "immediate",
                                          "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]


class CallbackManager:
    def __init__(self, app, frames, fig):
        self.app = app
        self.frames = frames
        self.fig = fig

    def register_callbacks(self):
        self.app.callback(
            Output('animation-graph', 'figure'),
            [Input('frame-slider', 'value')],
            [State('animation-graph', 'figure')])(self.update_figure)

        self.app.callback(
            Output('frame-slider', 'value'),
            [Input('frame-interval', 'n_intervals')],
            [State('frame-slider', 'value')])(self.advance_frame)

        self.app.callback(
            [Output('frame-interval', 'interval'), Output('frame-interval', 'n_intervals')],
            [Input('animation-graph', 'figure')])(self.update_interval)

    def update_figure(self, selected_frame, existing_figure):
        new_figure = go.Figure(data=self.frames[selected_frame]['data'], layout=existing_figure['layout'])
        if 'camera' in existing_figure['layout']['scene']:
            new_figure['layout']['scene']['camera']['eye'] = existing_figure['layout']['scene']['camera']['eye']
        else:
            # Camera key does not exist, setting a default value
            new_figure['layout']['scene']['camera'] = dict(eye=dict(x=1.25, y=1.25, z=1.25))

        new_figure.layout.updatemenus[0].buttons[0].args[1]['frame']['name'] = self.frames[selected_frame][
            'name']  # Update the frame
        return new_figure

    def advance_frame(self, n_intervals, current_frame):
        return (current_frame + 1) % len(self.frames)

    def update_interval(self, figure):
        playing = figure['layout']['updatemenus'][0]['buttons'][0]['args'][1]['frame']['duration'] > 0
        if playing:
            return 1000, 0  # 1000 milliseconds
        else:
            return 60 * 60 * 1000, 0  # effectively "paused" at 1 update per hour


class CaptureVolume3dViewer:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)
        self.data_loader = DataLoader(self.recording_folder_path)

    def load_data(self):
        data_by_frame = self.data_loader.load_data_by_frame()
        self.frames = FrameCreator.create_frames(data_by_frame)

    def create_app(self):
        self.load_data()

        app_layout_creator = AppLayoutCreator(self.frames)
        fig, layout = app_layout_creator.create_layout()

        app = Dash(__name__)
        app.layout = layout

        callback_manager = CallbackManager(app, self.frames, fig)
        callback_manager.register_callbacks()

        return app


if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(description='3D Viewer for Capture Volume.')
    # parser.add_argument('--path', required=True, help='Path to the recording folder.')
    # args = parser.parse_args()
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"

    viewer = CaptureVolume3dViewer(SAMPLE_DATA_PATH)
    app = viewer.create_app()
    app.run_server(debug=True)
