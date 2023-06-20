import logging

import plotly.graph_objects as go
from dash import dcc, html, Dash

# Silence the werkzeug logger
logging.getLogger('werkzeug').setLevel(logging.WARNING)


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
    def create_dash_app(figure, frames):
        app = Dash(__name__)

        app.layout = html.Div([
            dcc.Graph(id='animation-graph', figure=figure, style={'height': '100%', 'width': '100%'}),
            dcc.Slider(
                id='frame-slider',
                min=0,
                max=len(frames) - 1,
                value=0,
                step=1,
                marks={i: str(i) for i in range(len(frames))},
            ),
            html.Script("""
            const slider = document.getElementById('frame-slider');
            const graph = document.getElementById('animation-graph');

            graph.on('plotly_animated', () => {
                const currentFrame = graph._fullLayout.currentFrame;
                slider.value = currentFrame;
            });
            """)
        ])
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
