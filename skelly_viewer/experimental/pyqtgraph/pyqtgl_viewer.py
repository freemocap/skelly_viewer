import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore
import math
import time

app = pg.mkQApp("GLScatterPlotItem Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: Connected Spheres')
w.setCameraPosition(distance=50)

g = gl.GLGridItem()
w.addItem(g)

def generate_path(t):
    positions = np.zeros((24, 3))
    for i in range(24):
        angle = 2 * math.pi * i / 24 + t
        positions[i, 0] = 10 * math.sin(angle)
        positions[i, 1] = 10 * math.cos(angle)
        positions[i, 2] = math.sin(2 * angle)
    return positions

pos = generate_path(0)
size = np.full(24, 1)
color = np.array([[1.0, 0.0, 0.0, 0.5]] * 24)

sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
w.addItem(sp1)

start_time = time.time()

def update():
    global sp1, start_time
    t = (time.time() - start_time) * 0.1
    pos = generate_path(t)
    sp1.setData(pos=pos)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)

if __name__ == '__main__':
    pg.exec()
