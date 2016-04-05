#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np

import pyLeaflet


def example1(saveAs=None):
    N=1000

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
    x2 = 5.0 * np.random.randn(N) -84
    y2 = 2.0 * np.random.randn(N) +32
    colors = np.random.rand(N)
    size = np.pi * (15 * np.random.rand(N))**2

    t = np.linspace(1,100,len(x))
    t2 = np.linspace(1,100,len(x2))

    fig, (ax1,ax2,ax3) = plt.subplots(figsize=(18, 18),nrows=3,ncols=1)

    ax1.add_patch(patch)
    points = ax1.plot(x, y, 'b^', ms=10)
    line = ax1.plot(x, y, '-k')
    scatter = ax1.scatter(x2, y2, s=size, c=colors, alpha=0.5)
    # this should draw a black dot on top of the empire state building
    ax1.plot([-73.9857],[40.7484],'ro',ms=10)
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
    html = pyLeaflet.plotWithMap(fig,tile_layer = tile_layer,saveAs=saveAs)

    return html

def render_csv_file(fname,delimiter=',',saveAs=None, **kwargs):
    data = np.genfromtxt(fname,names=True,skip_header=0,delimiter=',')
    x, y =  data['lon'],data['lat']

    fig, ax1 = plt.subplots(figsize=(15, 18),nrows=1,ncols=1)

    # this plots the lines of the csv as markers, colored as a function
    # of the column `info1`, with a linear colormap blue->green

    kwargs['marker'] = 'o' if not kwargs.has_key('marker') else kwargs['marker']
    kwargs['s'] = [50]*len(x) if not kwargs.has_key('s') else kwargs['s']
    kwargs['cmap'] = \
        plt.get_cmap('winter') if not kwargs.has_key('cmap') else kwargs['cmap']
    kwargs['c'] = data['info1'] if not kwargs.has_key('c') else kwargs['c']
    kwargs['linewidths'] = \
        0 if not kwargs.has_key('linewidths') else kwargs['linewidths']

    print kwargs

    ax1.scatter(x, y, **kwargs)

    ax1.axis('equal')
    ax1.set_xlabel('longitude')
    ax1.set_ylabel('latitude')

    ###############
    ###############
    # tile_layer = "http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg"
    tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"
    html = pyLeaflet.plotWithMap(fig,tile_layer = tile_layer,saveAs=saveAs)

    return html


example1(saveAs="pyLeaflet_example.html")
# render_csv_file('example.csv',linewidths=0,marker='v')



