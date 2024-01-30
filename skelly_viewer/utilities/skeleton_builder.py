from typing import List, Tuple

import numpy as np
from rich.progress import track

def build_skeleton(
        skeleton_3d_frame_marker_xyz: np.ndarray,
        pose_estimation_connections: List[Tuple[int, int]]
        ) -> List[List[List[np.ndarray]]]:
    num_frames = skeleton_3d_frame_marker_xyz.shape[0]

    skeleton_connection_coordinates = []

    for frame in track(range(num_frames)):
        frame_connection_coordinates = []
        for connection in pose_estimation_connections:
            joint_1_coordinates = skeleton_3d_frame_marker_xyz[frame, connection[0], :]
            joint_2_coordinates = skeleton_3d_frame_marker_xyz[frame, connection[1], :]

            connection_coordinates = [joint_1_coordinates, joint_2_coordinates]

            frame_connection_coordinates.append(connection_coordinates)
        skeleton_connection_coordinates.append(frame_connection_coordinates)

    return skeleton_connection_coordinates
