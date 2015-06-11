#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np
import pyLeaflet

fig, ax = plt.subplots()

Path = mpath.Path
path_data = [
    (Path.MOVETO, (1.58-85, 35-2.57)),
    (Path.CURVE4, (0.35-85, 35-1.1)),
    (Path.CURVE4, (-1.85-85, 35+2.0)),
    (Path.CURVE4, (0.385-85, 35+2.0)),
    (Path.LINETO, (0.85-85, 35+1.15)),
    (Path.CURVE4, (2.2-85, 35+3.2)),
    (Path.CURVE4, (3-85, 35+0.05)),
    (Path.CURVE4, (2.0-85, 35-0.5)),
    (Path.CLOSEPOLY, (1.58-85, 35-2.57)),
    ]
codes, verts = zip(*path_data)
path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
ax.add_patch(patch)

# plot control points and connecting lines
x, y = zip(*path.vertices[:-1])
points = ax.plot(x, y, 'bo', ms=5)
line = ax.plot(x, y, '-k')

x2 = 2.5 * np.random.randn(200) -84
y2 = 2.0 * np.random.randn(200) +32
line2 = ax.plot(x2, y2, 'ro', ms=5)
ax.plot(x2, y2, '-g', ms=10)
ax.axis('equal')

###############
###############
# tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"
tile_layer = "http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg"
pyLeaflet.plotWithMap(fig,tile_layer = tile_layer,withAxes=False,withNonD3Elements=False)