from pathlib import Path
from typing import List, Dict

import numpy as np
from rich.progress import track

mediapipe_indices = ['nose',
                     'left_eye_inner',
                     'left_eye',
                     'left_eye_outer',
                     'right_eye_inner',
                     'right_eye',
                     'right_eye_outer',
                     'left_ear',
                     'right_ear',
                     'mouth_left',
                     'mouth_right',
                     'left_shoulder',
                     'right_shoulder',
                     'left_elbow',
                     'right_elbow',
                     'left_wrist',
                     'right_wrist',
                     'left_pinky',
                     'right_pinky',
                     'left_index',
                     'right_index',
                     'left_thumb',
                     'right_thumb',
                     'left_hip',
                     'right_hip',
                     'left_knee',
                     'right_knee',
                     'left_ankle',
                     'right_ankle',
                     'left_heel',
                     'right_heel',
                     'left_foot_index',
                     'right_foot_index']

mediapipe_connections = {'shoulders': ['left_shoulder', 'right_shoulder'],
                         'hips': ['left_hip', 'right_hip'],
                         'torso_left': ['left_shoulder', 'left_hip'],
                         'torso_right': ['right_shoulder', 'right_hip'],
                         'left_upper_arm': ['left_shoulder', 'left_elbow'],
                         'left_lower_arm': ['left_elbow', 'left_wrist'],
                         'left_upper_leg': ['left_hip', 'left_knee'],
                         'left_lower_leg': ['left_knee', 'left_ankle'],
                         'left_heel_connection': ['left_ankle', 'left_heel'],
                         'left_foot': ['left_heel', 'left_foot_index'],

                         'right_upper_arm': ['right_shoulder', 'right_elbow'],
                         'right_lower_arm': ['right_elbow', 'right_wrist'],
                         'right_upper_leg': ['right_hip', 'right_knee'],
                         'right_lower_leg': ['right_knee', 'right_ankle'],
                         'right_heel_connection': ['right_ankle', 'right_heel'],
                         'right_foot': ['right_heel', 'right_foot_index']}

reprojection_error_mediapipe_connections = {'left_upper_arm': ['left_shoulder', 'left_elbow'],
                                            'left_lower_arm': ['left_elbow', 'left_wrist'],
                                            'left_upper_leg': ['left_hip', 'left_knee'],
                                            'left_lower_leg': ['left_knee', 'left_ankle'],
                                            'left_foot': ['left_ankle', 'left_heel', 'left_foot_index'],
                                            'right_upper_arm': ['right_shoulder', 'right_elbow'],
                                            'right_lower_arm': ['right_elbow', 'right_wrist'],
                                            'right_upper_leg': ['right_hip', 'right_knee'],
                                            'right_lower_leg': ['right_knee', 'right_ankle'],
                                            'right_foot': ['right_ankle', 'right_heel', 'right_foot_index']}


def get_joint_coordinates_from_name(frame: int, joint_name: str, pose_estimation_markers, skeleton_3d_frame_marker_xyz):
    joint_index_number = pose_estimation_markers.index(joint_name)
    joint_coordinates = skeleton_3d_frame_marker_xyz[frame, joint_index_number, :]

    return joint_coordinates


def build_skeleton(skeleton_3d_frame_marker_xyz:np.ndarray,
                   pose_estimation_markers_list:List[str],
                   pose_estimation_connections_dict: Dict[str, List[str]]):
    num_frames = skeleton_3d_frame_marker_xyz.shape[0]

    skeleton_connection_coordinates = []

    for frame in track(range(num_frames)):
        this_frame_connection_dict = {}
        for connection in pose_estimation_connections_dict:
            joint_1_name = pose_estimation_connections_dict[connection][0]
            joint_2_name = pose_estimation_connections_dict[connection][1]

            joint_1_coordinates = get_joint_coordinates_from_name(frame, joint_1_name, pose_estimation_markers_list,
                                                                  skeleton_3d_frame_marker_xyz)
            joint_2_coordinates = get_joint_coordinates_from_name(frame, joint_2_name, pose_estimation_markers_list,
                                                                  skeleton_3d_frame_marker_xyz)

            this_connection_coordinates = [joint_1_coordinates, joint_2_coordinates]

            this_frame_connection_dict[connection] = this_connection_coordinates
        skeleton_connection_coordinates.append(this_frame_connection_dict)

    return skeleton_connection_coordinates


def get_mediapipe_indices(joint_center: str):
    return mediapipe_indices.index(joint_center)


if __name__ == '__main__':
    freemocap_data_folder_path = Path(r'D:\freemocap2022\FreeMocap_Data')
    sessionID = 'sesh_2022-09-29_17_29_31'
    data_array_folder = 'DataArrays'
    array_name = 'mediaPipeSkel_3d.npy'

    data_array_folder_path = freemocap_data_folder_path / sessionID / data_array_folder
    skel3d_raw_data = np.load(data_array_folder_path / array_name)
    skel_repro = np.load(data_array_folder_path / 'mediaPipeSkel_reprojErr.npy')
    # build_skeleton(skel3d_raw_data,mediapipe_indices,mediapipe_connections)
    # limb_repro = sum_reprojection_error_by_limb(skel_repro,mediapipe_indices,reprojection_error_mediapipe_connections)

    limb_repro = sum_reprojection_error_by_limb_reformat(skel_repro, mediapipe_indices,
                                                         reprojection_error_mediapipe_connections)
    # num_tracked_markers = get_number_of_tracked_markers(skel_repro,mediapipe_indices)
    f = 2
