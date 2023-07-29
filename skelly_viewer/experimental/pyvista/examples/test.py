from pyvista import examples
import numpy as np
import pyvista as pv

points = np.random.rand(100, 3)
mesh = pv.PolyData(points)
mesh.plot(point_size=10, style='points')

mesh = examples.load_hexbeam()
cpos = [(6.20, 3.00, 7.50),
        (0.16, 0.13, 2.65),
        (-0.28, 0.94, -0.21)]

pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, color='white')
pl.add_points(mesh.points, color='red',
              point_size=20)
pl.camera_position = cpos
pl.show()


mesh = examples.load_hexbeam()

pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, color='white')
pl.add_points(mesh.points, color='red', point_size=20)

single_cell = mesh.extract_cells(mesh.n_cells - 1)
pl.add_mesh(single_cell, color='pink', edge_color='blue',
            line_width=5, show_edges=True)

pl.camera_position = [(6.20, 3.00, 7.50),
                      (0.16, 0.13, 2.65),
                      (-0.28, 0.94, -0.21)]
pl.show()


mesh = examples.download_bunny_coarse()

pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, color='white')
pl.add_points(mesh.points, color='red',
              point_size=2)
pl.camera_position = [(0.02, 0.30, 0.73),
                      (0.02, 0.03, -0.022),
                      (-0.03, 0.94, -0.34)]
pl.show()


import pyvista as pv
from pyvista import examples
uni = examples.load_uniform()

pl = pv.Plotter(shape=(1, 2), border=False)
pl.add_mesh(uni, scalars='Spatial Point Data', show_edges=True)
pl.subplot(0, 1)
pl.add_mesh(uni, scalars='Spatial Cell Data', show_edges=True)
pl.show()



cube = pv.Cube()
cube.cell_data['myscalars'] = range(6)

other_cube = cube.copy()
other_cube.point_data['myscalars'] = range(8)

pl = pv.Plotter(shape=(1, 2), border_width=1)
pl.add_mesh(cube, cmap='coolwarm')
pl.subplot(0, 1)
pl.add_mesh(other_cube, cmap='coolwarm')
pl.show()


import pyvista as pv
from pyvista import examples

# download an example and display it using physically based rendering.
mesh = examples.download_lucy()
mesh.plot(color='lightgrey', pbr=True, metallic=0.2,
          jupyter_backend='pythreejs')


from pyvista import demos

# basic glyphs demo
mesh = demos.glyphs(2)

text = demos.logo.text_3d("I'm interactive!", depth=0.2)
text.points *= 0.1
text.translate([0, 1.4, 1.5], inplace=True)
mesh += text
mesh['Example Scalars'] = mesh.points[:, 0]

mesh.plot(cpos='xy', jupyter_backend='ipygany', show_scalar_bar=True)




from math import sin, cos, radians
import pyvista as pv

# Create source to ray trace
sphere = pv.Sphere(radius=0.85)

# Define a list of origin points and a list of direction vectors for each ray
vectors = [ [cos(radians(x)), sin(radians(x)), 0] for x in range(0, 360, 5)]
origins = [[0, 0, 0]] * len(vectors)

# Perform ray trace
points, ind_ray, ind_tri = sphere.multi_ray_trace(origins, vectors)

# Create geometry to represent ray trace
rays = [pv.Line(o, v) for o, v in zip(origins, vectors)]
intersections = pv.PolyData(points)

# Render the result
p = pv.Plotter()
p.add_mesh(sphere,
           show_edges=True, opacity=0.5, color="w",
           lighting=False, label="Test Mesh")
p.add_mesh(rays[0], color="blue", line_width=5, label="Ray Segments")
for ray in rays[1:]:
    p.add_mesh(ray, color="blue", line_width=5)
p.add_mesh(intersections, color="maroon",
           point_size=25, label="Intersection Points")
p.add_legend()
p.show()





x = np.arange(-10, 10, 0.5)
y = np.arange(-10, 10, 0.5)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r)

# Create and structured surface
grid = pv.StructuredGrid(x, y, z)
grid.plot()

# Create a plotter object and set the scalars to the Z height
plotter = pv.Plotter(notebook=False, off_screen=True)
plotter.add_mesh(
    grid,
    scalars=z.ravel(),
    lighting=False,
    show_edges=True,
    scalar_bar_args={"title": "Height"},
    clim=[-1, 1],
)

# Open a gif
plotter.open_gif("wave.gif")
x = np.arange(-10, 10, 0.5)
y = np.arange(-10, 10, 0.5)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r)

# Create and structured surface
grid = pv.StructuredGrid(x, y, z)
grid.plot()
pts = grid.points.copy()

# Update Z and write a frame for each updated position
nframe = 15
for phase in np.linspace(0, 2 * np.pi, nframe + 1)[:nframe]:
    z = np.sin(r + phase)
    pts[:, -1] = z.ravel()
    plotter.update_coordinates(pts, render=False)
    plotter.update_scalars(z.ravel(), render=False)

    # Write a frame. This triggers a render.
    plotter.write_frame()

# Closes and finalizes movie
plotter.close()

# Create a plotter object and set the scalars to the Z height
plotter = pv.Plotter(notebook=False, off_screen=True)
plotter.add_mesh(
    grid,
    scalars=z.ravel(),
    lighting=False,
    show_edges=True,
    scalar_bar_args={"title": "Height"},
    clim=[-1, 1],
)

# Open a gif
plotter.open_gif("wave.gif")

pts = grid.points.copy()

# Update Z and write a frame for each updated position
nframe = 15
for phase in np.linspace(0, 2 * np.pi, nframe + 1)[:nframe]:
    z = np.sin(r + phase)
    pts[:, -1] = z.ravel()
    plotter.update_coordinates(pts, render=False)
    plotter.update_scalars(z.ravel(), render=False)

    # Write a frame. This triggers a render.
    plotter.write_frame()

# Closes and finalizes movie
plotter.close()