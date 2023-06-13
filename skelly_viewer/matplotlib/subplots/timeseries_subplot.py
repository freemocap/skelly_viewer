from typing import List

from skelly_viewer.matplotlib.subplots.base_subplot import BasePlot, PLOT_COLOR


class TimeseriesSubplot(BasePlot):
    def __init__(self, frames:List[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = frames
        self.axis = self.figure.add_subplot(self.grid_spec[self.subplot_index[0], self.subplot_index[1]])
        self.timeseries_data = self.com_xyz[:,2]
        self.line, = self.axis.plot(self.timeseries_data, color=PLOT_COLOR)
        self.vertical_line = self.axis.axvline(x=0, color='k')

    def clear(self):
        self.axis.clear()

    def set_axis_limits(self):
        self.axis.set_xlim(self.frames[0], self.frames[-1])
        self.axis.set_ylim(min(self.timeseries_data[self.frames]), max(self.timeseries_data[self.frames]))

    def animate(self, frame_number):
        self.clear()
        self.set_axis_limits()
        self.line, = self.axis.plot(self.timeseries_data, color=PLOT_COLOR)
        self.vertical_line = self.axis.axvline(x=frame_number, color='r')