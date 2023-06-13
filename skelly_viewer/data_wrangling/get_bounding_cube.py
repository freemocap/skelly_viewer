from typing import List, Tuple

import numpy as np


def get_bounding_cube(data_xyz: np.ndarray,
                      buffer: float = 1000)->dict:

    x_min, x_max = np.min(data_xyz[:, 0]), np.max(data_xyz[:, 0])
    y_min, y_max = np.min(data_xyz[:, 1]), np.max(data_xyz[:, 1])
    z_min, z_max = np.min(data_xyz[:, 2]), np.max(data_xyz[:, 2])

    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    max_range = max(x_range, y_range, z_range)+buffer

    x_mid = (x_min + x_max) / 2
    y_mid = (y_min + y_max) / 2
    z_mid = (z_min + z_max) / 2

    x_min, x_max = x_mid - max_range / 2, x_mid + max_range / 2
    y_min, y_max = y_mid - max_range / 2, y_mid + max_range / 2
    z_min, z_max = z_mid - max_range / 2, z_mid + max_range / 2

    return {"x": [x_min, x_max], "y": [y_min, y_max], "z": [z_min, z_max]}
