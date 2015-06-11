#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np

from mpld3 import plugins,utils
import pyLeaflet

class DragPlugin(plugins.PluginBase):
    JAVASCRIPT = r"""
    mpld3.register_plugin("drag", DragPlugin);
    DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    DragPlugin.prototype.constructor = DragPlugin;
    DragPlugin.prototype.requiredProps = ["id"];
    DragPlugin.prototype.defaultProps = {}
    function DragPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
        mpld3.insert_css("#" + fig.figid + " path.dragging",
                         {"fill-opacity": "1.0 !important",
                          "stroke-opacity": "1.0 !important"});
    };

    DragPlugin.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);

        var drag = d3.behavior.drag()
            .origin(function(d) { return {x:obj.ax.x(d[0]),
                                          y:obj.ax.y(d[1])}; })
            .on("dragstart", dragstarted)
            .on("drag", dragged)
            .on("dragend", dragended);

        obj.elements()
           .data(obj.offsets)
           .style("cursor", "default")
           .call(drag);

        function dragstarted(d) {
          d3.event.sourceEvent.stopPropagation();
          d3.select(this).classed("dragging", true);
        }

        function dragged(d, i) {
          d[0] = obj.ax.x.invert(d3.event.x);
          d[1] = obj.ax.y.invert(d3.event.y);
          d3.select(this)
            .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
        }

        function dragended(d) {
          d3.select(this).classed("dragging", false);
        }
    }
    """

    def __init__(self, points):
        if isinstance(points, mpl.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "drag",
                      "id": utils.get_id(points, suffix)}

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

plugins.connect(fig, DragPlugin(points[0]))
###############
###############
# tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"
tile_layer = "http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg"
pyLeaflet.plotWithMap(fig,tile_layer = tile_layer,withAxes=False,withNonD3Elements=False)