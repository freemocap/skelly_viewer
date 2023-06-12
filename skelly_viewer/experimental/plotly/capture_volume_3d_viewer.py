from pathlib import Path
from typing import Union

from dash import dcc, Dash, html, Input, Output, State
from plotly import graph_objects as go

from skelly_viewer.experimental.plotly.plotly_dash_setup import DataLoader, FrameCreator

SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"


class CaptureVolume3dViewer:
    def __init__(self, recording_folder_path: Union[str, Path]):
        self.recording_folder_path = Path(recording_folder_path)
        self.ax_range = 2500
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

        fig_dict = {
            "data": [self.frames[0]['data'][0]],
            "layout": {
                "scene": {
                    "xaxis": dict(self.axis_props, range=[-self.ax_range, self.ax_range]),
                    "yaxis": dict(self.axis_props, range=[-self.ax_range, self.ax_range]),
                    "zaxis": dict(self.axis_props, range=[-self.ax_range, self.ax_range]),
                    "aspectmode": 'cube'
                },
                "updatemenus": [
                    {
                        "buttons": [
                            {
                                "args": [None, {"frame": {"duration": 30, "redraw": False},
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
                ],
            },
            "frames": self.frames
        }

        fig = go.Figure(fig_dict)

        app = Dash(__name__)
        app.layout = html.Div([
            dcc.Graph(id='animation-graph', figure=fig, style={'height': '100%', 'width': '100%'}),
            dcc.Slider(
                id='frame-slider',
                min=0,
                max=len(self.frames) - 1,
                value=0,
            ),
            dcc.Interval(
                id='frame-interval',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ])

        @app.callback(
            Output('animation-graph', 'figure'),
            [Input('frame-slider', 'value')],
            [State('animation-graph', 'figure')])
        def update_figure(selected_frame, existing_figure):
            new_figure = go.Figure(data=self.frames[selected_frame]['data'],
                                   layout=existing_figure['layout'])
            try:
                new_figure['layout']['scene']['camera']['eye'] = existing_figure['layout']['scene']['camera']['eye']
            except KeyError:
                # Camera key does not exist, setting a default value
                new_figure['layout']['scene']['camera'] = dict(eye=dict(x=1.25, y=1.25, z=1.25))

            new_figure.layout.updatemenus[0].buttons[0].args[1]['frame']['name'] = self.frames[selected_frame][
                'name']  # Update the frame
            return new_figure

        @app.callback(
            Output('frame-slider', 'value'),
            [Input('frame-interval', 'n_intervals')],
            [State('frame-slider', 'value')])
        def advance_frame(n_intervals, current_frame):
            return (current_frame + 1) % len(self.frames)

        @app.callback(
            [Output('frame-interval', 'interval'), Output('frame-interval', 'n_intervals')],
            [Input('animation-graph', 'figure')])
        def update_interval(figure):
            playing = figure['layout']['updatemenus'][0]['buttons'][0]['args'][1]['frame']['duration'] > 0
            if playing:
                return 1000, 0  # 1000 milliseconds
            else:
                return 60 * 60 * 1000, 0  # effectively "paused" at 1 update per hour

        return app


if __name__ == "__main__":
    recording_folder_path = SAMPLE_DATA_PATH
    viewer = CaptureVolume3dViewer(recording_folder_path)
    app = viewer.create_app()
    app.run_server(debug=True)
