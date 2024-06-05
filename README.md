# Installation

Create a conda environment using Python 3.11 (recommended, untested on other versions) and activate your conda environment 

Install skelly_viewer using `pip install skelly_viewer`

# Usage

After installing, in your conda terminal (with the right environment active), type `skelly_viewer'

You should see a GUI pop up with an empty graph, a slider, and two buttons

Click the `Load a session folder` button, and select a session folder that you would like to view the data from using the folder dialog 
(NOTE: As of right now, this viewer only works with pre-alpha labeled, post-processed data (it looks the `DataArrays` folder with a file 
called `mediaPipeSkel_3d_origin_aligned.npy` inside of it)

You can move the slider, and the 3D graph should show your skeleton

If you hit the `Load Videos` button on the side, select a folder of videos within your current session. When you move the slider, the videos
should load in and appear on the right hand side 



