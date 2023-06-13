from typing import Union

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from skelly_viewer.data_wrangling.data_loader import DataLoader
from skelly_viewer.data_wrangling.get_bounding_cube import get_bounding_cube
import numpy as np

PLOT_COLOR = 'purple'
MARKER_SIZE = 10

class BasePlot:
    def __init__(self, figure: Figure,
                 grid_spec: GridSpec,
                 subplot_index: tuple,
                 data_loader: DataLoader):
        self.figure = figure
        self.grid_spec = grid_spec
        self.subplot_index = subplot_index
        self.data_by_frame = data_loader.data_by_frame["data_by_frame"]
        self.data_by_trajectory = data_loader.data_by_trajectory
        self.info = data_loader.data_by_frame["info"]
        self.com_xyz = data_loader.center_of_mass_xyz
        self.axis_limits = get_bounding_cube(self.com_xyz)

