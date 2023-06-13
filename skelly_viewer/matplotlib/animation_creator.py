import logging
from pathlib import Path
from typing import Union, Tuple

import matplotlib.animation as animation
import numpy as np

from skelly_viewer.matplotlib.figure_maker import FigureMaker

mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

FRAME_INTERVAL = 1000 / 30

from skelly_viewer.data_wrangling.data_loader import DataLoader


class AnimationCreator:
    def __init__(self,
                 recording_path: Union[str, Path],
                 frame_range: Tuple[int, int] = None):

        data_loader = DataLoader(recording_path)

        self.recording_name = Path(recording_path).name

        if frame_range:
            self.frame_numbers = list(np.arange(frame_range[0], frame_range[1] + 1))
            self.output_file = Path(recording_path) / f"{self.recording_name}_animation_frames_{frame_range[0]}-{frame_range[1]}.mp4"

        else:
            self.frame_numbers = np.arange(data_loader.number_of_frames).tolist()
            self.output_file = Path(recording_path) / f"{self.recording_name}_animation.mp4"

        self.figure_maker = FigureMaker(data_loader=data_loader,
                                        frames=self.frame_numbers)






    def update_figure(self, frame_number: Union[str, int]):
        # If the states have been stored, apply them in each frame

        self.figure_maker.figure.suptitle(f"{self.recording_name} - Frame {frame_number}")
        self.figure_maker.update_figure(frame_number=frame_number)

    def show_middle_frame(self):
        # Calculate the middle frame number
        middle_frame_number = len(self.frame_numbers) // 2

        # Update the figure with the middle frame
        self.update_figure(middle_frame_number)

        # Display the figure
        self.figure_maker.show()
    def start_animation(self):
        self.animation = animation.FuncAnimation(fig=self.figure_maker.figure,
                                                 func=self.update_figure,
                                                 frames=self.frame_numbers,
                                                 interval=FRAME_INTERVAL,
                                                 blit=False)
        self.figure_maker.show()


    def save(self):
        self.animation.save(str(self.output_file), writer='ffmpeg', fps=30)


if __name__ == "__main__":
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"

    # recording_path_in = SAMPLE_DATA_PATH
    recording_path_in = r"D:\Dropbox\FreeMoCapProject\freemocap_validation_data\2023-05-18-MDN-NIH-Walk\processed_freemocap_data\sesh_2023-05-17_15_36_03_MDN_OneLeg_Trial1"

    animator = AnimationCreator(recording_path=recording_path_in,
                                frame_range=(500, 1000)
                                )
    # animator.show_middle_frame()

    print("Showing animation...")
    animator.start_animation()

    print("Saving animation...")
    animator.save()
    print(f"Animation saved to: {animator.output_file}")
