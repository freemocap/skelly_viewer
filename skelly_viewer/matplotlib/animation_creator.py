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
            self.frames = np.arange(frame_range[0], frame_range[1] + 1).tolist()
            self.output_file = Path(recording_path) / f"{self.recording_name}_animation_frames_{frame_range[0]}-{frame_range[1]}.mp4"

        else:
            self.frames = np.arange(data_loader.number_of_frames).tolist()
            self.output_file = Path(recording_path) / f"{self.recording_name}_animation.mp4"

        self.figure_maker = FigureMaker(data_loader=data_loader,
                                        frames=self.frames)


        self.animation = animation.FuncAnimation(fig=self.figure_maker.figure,
                                                 func=self.update_figure,
                                                 frames=self.frames,
                                                 interval=FRAME_INTERVAL,
                                                 blit=False)

        self.animation_running = True
        self.animation.event_source.stop()  # Initially stop the animation


    def toggle_animation(self):
        if self.animation_running:
            self.animation.event_source.stop()
            self.animation_running = False
        else:
            self.animation.event_source.start()
            self.animation_running = True

    def update_figure(self, frame_number: Union[str, int]):
        # If the states have been stored, apply them in each frame

        self.figure_maker.figure.suptitle(f"{self.recording_name} - Frame {frame_number}")
        self.figure_maker.update_figure(frame_number=frame_number)



    def show(self):
        self.figure_maker.show()


    def save(self):
        self.animation.save(str(self.output_file), writer='ffmpeg', fps=30)


if __name__ == "__main__":
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"

    # recording_path_in = SAMPLE_DATA_PATH
    recording_path_in = r"D:\Dropbox\FreeMoCapProject\freemocap_validation_data\2023-05-18-MDN-NIH-Walk\processed_freemocap_data\sesh_2023-05-17_13_37_32_MDN_treadmill_1"

    animator = AnimationCreator(recording_path=recording_path_in,
                                frame_range=(100, 200)
                                )


    print("Showing animation...")
    animator.show()

    print("Saving animation...")
    animator.save()
    print(f"Animation saved to: {animator.output_file}")
