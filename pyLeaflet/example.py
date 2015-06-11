#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np
import pyLeaflet

N=200

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

# plot control points and connecting lines
x, y = zip(*path.vertices[:-1])
x2 = 2.5 * np.random.randn(N) -84
y2 = 2.0 * np.random.randn(N) +32

t = np.linspace(1,100,len(x))
t2 = np.linspace(1,100,len(x2))

fig, (ax1,ax2,ax3) = plt.subplots(figsize=(18, 18),nrows=3,ncols=1)

ax1.add_patch(patch)
points = ax1.plot(x, y, 'bo', ms=5)
line = ax1.plot(x, y, '-k')
line2 = ax1.plot(x2, y2, 'ro', ms=5)
ax1.plot(x2, y2, '--g', ms=10)
ax1.axis('equal')
ax1.set_xlabel('longitude')
ax1.set_ylabel('latitude')

ax2.plot(t,x,'-k')
ax2.plot(t2,x2,'--g')
ax2.set_xlabel('t')
ax2.set_ylabel('x')
ax2.legend(['x','x2'])

ax3.plot(t,y,'-k')
ax3.plot(t2,y2,'--g')
ax3.set_xlabel('t')
ax3.set_ylabel('y')
ax3.legend(['y','y2'])




###############
###############
# tile_layer = "http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg"
tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"
pyLeaflet.plotWithMap(fig,tile_layer = tile_layer)


fout = open('index.html','w')
fout.write(html)
fout.close()