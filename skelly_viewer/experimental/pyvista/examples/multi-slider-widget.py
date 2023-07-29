import pyvista as pv
import numpy as np

# Define parameters for circular motion
radius_of_track = 2.0
angle = 0

# Create a sphere
sphere = pv.Sphere(radius=0.5)

# Create a circular ring to represent the track
track = pv.Cylinder(center=[0, 0, 0], radius=radius_of_track, height=0.1, direction=[0, 0, 1])

# Create a plotter
p = pv.Plotter()

# Add the track and the sphere to the plotter
p.add_mesh(track, color="gray")
p.add_mesh(sphere, show_edges=True)

# Function to update the sphere's position around the circular track
def update_sphere(angle):
    x = radius_of_track * np.cos(np.radians(angle))
    y = radius_of_track * np.sin(np.radians(angle))
    sphere.points[:, 0] = x + sphere.points[:, 0] - sphere.center[0]
    sphere.points[:, 1] = y + sphere.points[:, 1] - sphere.center[1]
    sphere.center = [x, y, 0]

# Open the plotter and set up the camera
p.show(auto_close=False, interactive=False)
p.camera_position = [(5, 5, 5), (0, 0, 0), (0, 0, 1)]

# Loop to animate the sphere
for angle in range(360):
    update_sphere(angle)
    p.update()
    p.reset_camera()

# Close the plotter
p.close()
