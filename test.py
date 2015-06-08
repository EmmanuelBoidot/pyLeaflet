#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

import mpld3
from mpld3 import plugins, utils

import pyLeaflet

fig, ax = plt.subplots()

Path = mpath.Path
path_data = [
    (Path.MOVETO, (1.58-75, 35-2.57)),
    (Path.CURVE4, (0.35-75, 35-1.1)),
    (Path.CURVE4, (-1.75-75, 35+2.0)),
    (Path.CURVE4, (0.375-75, 35+2.0)),
    (Path.LINETO, (0.85-75, 35+1.15)),
    (Path.CURVE4, (2.2-75, 35+3.2)),
    (Path.CURVE4, (3-75, 35+0.05)),
    (Path.CURVE4, (2.0-75, 35-0.5)),
    (Path.CLOSEPOLY, (1.58-75, 35-2.57)),
    ]
codes, verts = zip(*path_data)
path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
ax.add_patch(patch)

# plot control points and connecting lines
x, y = zip(*path.vertices[:-1])
points = ax.plot(x, y, 'bo', ms=10)
line = ax.plot(x, y, '-k')

ax.axis('equal')


###############
###############
# mpld3.show(fig)
# pyLeaflet.plotWithMap(fig)
pyLeaflet.plotWithMap(fig,tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg",lat=
35.256000, lon=-79.786989,zoom=6,withAxes=True)