from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation
from typing import List, Tuple
from mpl_toolkits.mplot3d import Axes3D

from skelly_viewer.utilities.load_sample_data import get_sample_data_path


class SkeletonOrienter:
    def __init__(self, points: np.ndarray):
        if len(points.shape) > 2:
            points_marker_xyz = points.reshape(-1, 3)  # collapse into a 3 column vector
        else:
            points_marker_xyz = points
        self.points_marker_xyz = points_marker_xyz
        self.rotation = None
        self.bottom_point = None

    def calculate_rotation(self, top_point_index: int, bottom_point_index: int, target_vector: np.ndarray):
        top_point = self.points_marker_xyz[top_point_index, :]
        self.bottom_point = self.points_marker_xyz[bottom_point_index, :]
        axis = top_point - self.bottom_point
        axis /= np.linalg.norm(axis)

        # Define rotation
        rotation_vector = np.cross(axis, target_vector)
        rotation_angle = np.arccos(np.dot(axis, target_vector))
        self.rotation = Rotation.from_rotvec(rotation_vector * rotation_angle)

    def apply_rotation(self, points: np.ndarray) -> np.ndarray:
        if self.rotation is None or self.bottom_point is None:
            raise Exception("Please calculate rotation first.")

        # Reshape points to 2D array (N, 3)
        original_shape = points.shape
        points = points.reshape(-1, 3)

        # Apply rotation
        new_points = self.rotation.apply(points - self.bottom_point) + self.bottom_point

        # Reshape back to original shape
        new_points = new_points.reshape(original_shape)

        return new_points


if __name__ == "__main__":
    import matplotlib.pyplot as plt


    sample_data_path = get_sample_data_path()

    points_path = str(Path(sample_data_path)/"output_data"/"mediapipe_body_3d_xyz.npy")
    points = np.load(points_path)

    point_cloud = SkeletonOrienter(points)
    top_idx = 2
    bottom_idx = 0
    target_vector = np.array([0, 0, 1])

    point_cloud.calculate_rotation(top_idx, bottom_idx, target_vector)
    oriented_points = point_cloud.apply_rotation(points)

    # Imagine you have new points to rotate
    new_points = np.array(np.random.rand(50, 3))
    oriented_new_points = point_cloud.apply_rotation(new_points)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    frame_idx = int(points.shape[0]/2) # middle frame

    # Plot the original points
    ax.scatter(*points[frame_idx].T, c="b", marker="o", alpha=0.1, label="Original")
    ax.scatter(*points[frame_idx, [top_idx, bottom_idx]].T, c="g", marker="o")
    ax.plot(*points[frame_idx, [top_idx, bottom_idx]].T, c="g")

    # Plot the oriented points
    ax.scatter(*oriented_points[frame_idx].T, c="r", marker="^", alpha=0.1, label="Oriented")
    ax.scatter(*oriented_points[frame_idx, [top_idx, bottom_idx]].T, c="purple", marker="^")
    ax.plot(*oriented_points[frame_idx, [top_idx, bottom_idx]].T, c="purple")

    # Plot the new points (in yellow)
    ax.scatter(*new_points.T, c="y", marker="o", alpha=0.1, label="New points")
    ax.scatter(*oriented_new_points.T, c="orange", marker="^", alpha=0.1, label="Oriented new points")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()

    plt.show()
