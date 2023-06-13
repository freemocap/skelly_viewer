
from skelly_viewer.matplotlib.subplots.base_subplot import BasePlot, PLOT_COLOR


class TimeseriesSubplot(BasePlot):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ax = self.figure.add_subplot(self.grid_spec[self.subplot_index[0], self.subplot_index[1]])
        self.timeseries_data = self.com_xyz[:,2]
        self.line, = self.ax.plot(self.timeseries_data, color=PLOT_COLOR)
        self.vertical_line = self.ax.axvline(x=0, color='k')

    def clear(self):
        self.ax.clear()

    def set_axis_limits(self):
        self.ax.set_xlim(0, len(self.timeseries_data))
        self.ax.set_ylim(min(self.timeseries_data), max(self.timeseries_data))

    def animate(self, frame_number):
        self.clear()
        self.set_axis_limits()
        self.line, = self.ax.plot(self.timeseries_data, color=PLOT_COLOR)
        self.vertical_line = self.ax.axvline(x=frame_number, color='r')