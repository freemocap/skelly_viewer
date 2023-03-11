import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Generate sample data with 3D point trajectories and timestamps
n_frames = 100
t = np.linspace(0, 2*np.pi, n_frames)
x = np.sin(t)
y = np.cos(t)
z = np.sin(2*t)
timestamp = pd.date_range('2022-01-01', periods=n_frames, freq='50ms')
df = pd.DataFrame({'x': x, 'y': y, 'z': z, 'timestamp': timestamp, 'frame_number': np.arange(n_frames)})

# Convert the timestamp column to a string representation
df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')

# Create a scatter 3D plot using Plotly Express, with the 'frame_number' column as the animation frame
fig = px.scatter_3d(df, x='x', y='y', z='z', color='frame_number', animation_frame='timestamp')

# Create a line 3D plot to show the closed curve trajectory
fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(width=5, color='black')))

# Create a Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
