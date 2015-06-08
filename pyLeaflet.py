import os
import random
import jinja2
import json
import mpld3
from mpld3 import urls
from mpld3.utils import get_id,write_ipynb_local_js
from mpld3.mpld3renderer import MPLD3Renderer
from mpld3.mplexporter import Exporter
from mpld3._server import serve_and_open

MAP_HTML = jinja2.Template("""
<script type="text/javascript" src="{{ d3_url }}"></script>
<script type="text/javascript" src="{{ mpld3_url }}"></script>
<script type='text/javascript' src='http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js'></script>
<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" type="text/css"/>

<style>
{{pyLeaflet_css}}
{{ extra_css }}
</style>

<div id="map-container">
    <div id="map-header"></div>
    <div id="map" class="column">
        <div id="pop-up">
            <div id="pop-up-title"></div>
            <div id="pop-up-content"></div>
        </div>
    </div>
</div>

<!-- <div id={{ figid }}></div> -->

<script>

{{leaflet_init_js}}

!function(mpld3){
    {{pyLeaflet_js}}
    {{ extra_js }}
}(mpld3);

var mdata = {{ figure_json }};
pt0 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ])
pt1 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ])
 m0 = new L.Marker([ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ]);
 m1 = new L.Marker([ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ]);
 map.addLayer(m0)
 map.addLayer(m1)
mheight = pt0.y-pt1.y
mwidth = pt1.x-pt0.x

mdata.height = mheight
mdata.width = mwidth
mdata.axes[0].bbox = [0, 0, 1, 1]

g.attr("transform", "translate(" + pt0.x + "," + pt1.y + ")").attr("width", mwidth).attr("height", mheight).attr("class", "mpld3-baseaxes");

pyLeaflet.draw_figure({{ figid }}, mdata);

map.on('zoomstart',function() {
  g.selectAll('.mpld3-baseaxes').remove()
})

map.on('zoomend', function() {
pt0 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ])
pt1 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ])
mheight = pt0.y-pt1.y
mwidth = pt1.x-pt0.x

mdata.height = mheight
mdata.width = mwidth

withAxes = {{withAxesStr}};

pyLeaflet.draw_figure({{ figid }}, mdata, withAxes);
});
</script>
""")

def plotWithMap(fig,tile_layer = "http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png",lat=37,lon=-90,zoom=4,withAxes=False, **kwargs):
  d3_url = urls.D3_URL
  mpld3_url = urls.MPLD3_URL
  # d3_url, mpld3_url = write_ipynb_local_js()

  figid = 'fig_' + get_id(fig) + str(int(random.random() * 1E10))

  renderer = MPLD3Renderer()
  Exporter(renderer, close_mpl=False).run(fig)

  fig, figure_json, extra_css, extra_js = renderer.finished_figures[0]

  extra_css = ""
  extra_js = ""
  with open('pyLeaflet.js','r') as f:
    pyLeaflet_js = f.read()
  with open('pyLeaflet.css','r') as f:
    pyLeaflet_css = f.read()

  if withAxes:
    withAxesStr="True"
  else:
    withAxesStr="False"

  leaflet_init_js = """
    var width = 800,
    height = 500;

    var mouseLat = %d;
    var mouseLng = %d;


    /*******************************************************************************
    *
    * Initialize map layout
    *
    *******************************************************************************/
    var map = L.map('map').setView([mouseLat, mouseLng],%d);
    map.scrollWheelZoom.disable();

    L.tileLayer('%s', {
        attribution: '',
        maxZoom: 18
    }).addTo(map);

    // Use Leaflet to implement a D3 geometric transformation.
    function projectPoint(x, y) {
      var point = map.latLngToLayerPoint(new L.LatLng(x, y));
      this.stream.point(point.x, point.y);
    }

    var transform = d3.geo.transform({point: projectPoint});
    var path = d3.geo.path().projection(transform);


    var svg = d3.select(map.getPanes().overlayPane).append('svg').attr('width',5000).attr('height',3000);
    var g   = svg.append('g').attr('class', 'leaflet-zoom-hide').attr('id','%s');

    """%(lat,lon,zoom,tile_layer,figid)
  # tile_layer = "http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png"
  # tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"

  kwargs['mpld3_url'] = os.path.dirname(mpld3.__file__)+'/js/mpld3.js'
  kwargs['d3_url'] = os.path.dirname(mpld3.__file__)+'/js/d3.js'
  files = {os.path.dirname(mpld3.__file__)+'/js/mpld3.js': ["text/javascript",
                         open(urls.MPLD3_LOCAL, 'r').read()],
           os.path.dirname(mpld3.__file__)+'/js/d3.js': ["text/javascript",
                      open(urls.D3_LOCAL, 'r').read()]}

  html = MAP_HTML.render(figid=json.dumps(figid),
                         d3_url=d3_url,
                         mpld3_url=mpld3_url,
                         figure_json=json.dumps(figure_json),
                         extra_css=extra_css,
                         extra_js=extra_js,
                         pyLeaflet_js=pyLeaflet_js,
                         pyLeaflet_css=pyLeaflet_css,
                         leaflet_init_js=leaflet_init_js,
                         tile_layer=tile_layer,
                         withAxesStr=withAxesStr)

  serve_and_open(html, ip='localhost', port=8888, n_retries=50, files=files)