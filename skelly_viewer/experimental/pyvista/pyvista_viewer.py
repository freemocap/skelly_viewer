import pyvista as pv
import numpy as np


class AnimatedScatterPlot:
    def __init__(self, num_points: int = 100):
        """Initialize the animated scatter plot.

        Args:
            num_points (int, optional): Number of points in the scatter plot. Defaults to 100.
        """
        self.num_points = num_points
        self.points = np.random.rand(num_points, 3) * 10  # Initial random points
        self.plotter = pv.Plotter()
        self.scatter = self.plotter.add_mesh(pv.PolyData(self.points), point_size=10, render_points_as_spheres=True)

    def update_points(self):
        """Update the points to create the animation effect."""
        self.points += np.random.randn(*self.points.shape) * 0.1  # Add some random noise
        self.scatter.points = self.points

    def animate(self, n_frames: int = 100):
        """Run the animation.

        Args:
            n_frames (int, optional): Number of frames in the animation. Defaults to 100.
        """
        for i in range(n_frames):
            self.plotter.update_scalars(self.points)
            self.update_points()
            self.plotter.render()


if __name__ == '__main__':
    scatter_plot = AnimatedScatterPlot()
    scatter_plot.plotter.show(auto_close=False)
    scatter_plot.animate()
