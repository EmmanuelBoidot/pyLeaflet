import os
import random
import jinja2
import json
import mpld3
from mpld3 import urls
from mpld3.utils import get_id
from mpld3.mpld3renderer import MPLD3Renderer
from mpld3.mplexporter import Exporter
from mpld3._server import serve_and_open

MAP_HTML = jinja2.Template("""
<script type="text/javascript">{{ d3_js }}</script>
<script type="text/javascript">{{ mpld3_js }}</script>
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

<div id={{ figid }} style="width:90%; margin:0 auto;"></div>

<script>

{{leaflet_init_js}}

var mdata = {{ figure_json }};
// This is so that the lat lon figure appears last
var mpld3_data = mdata;
if (mpld3_data.axes.length>1){
  var n = mpld3_data.axes.length;
  var tmp_bbox = mpld3_data.axes[n-1].bbox;
  mpld3_data.axes.forEach(function(a,i){
    if(i<=n-2){
      mpld3_data.axes[n-i-1].bbox = mpld3_data.axes[n-i-2].bbox;
    }
  })
  mpld3_data.axes[0].bbox = tmp_bbox;
}
function mpld3_load_lib(url, callback){
  var s = document.createElement('script');
  s.src = url;
  s.async = true;
  s.onreadystatechange = s.onload = callback;
  s.onerror = function(){console.warn("failed to load library " + url);};
  document.getElementsByTagName("head")[0].appendChild(s);
}

if(typeof(mpld3) !== "undefined" && mpld3._mpld3IsLoaded){
   // already loaded: just create the figure
   !function(mpld3){
       {{ extra_js }}
       mpld3.draw_figure({{ figid }}, mpld3_data);
   }(mpld3);
}else if(typeof define === "function" && define.amd){
   // require.js is available: use it to load d3/mpld3
   require.config({paths: {d3: "{{ d3_url[:-3] }}"}});
   require(["d3"], function(d3){
      window.d3 = d3;
      mpld3_load_lib("{{ mpld3_url }}", function(){
         {{ extra_js }}
         mpld3.draw_figure({{ figid }}, mpld3_data);
      });
    });
}else{
    // require.js not available: dynamically load d3 & mpld3
    mpld3_load_lib("{{ d3_url }}", function(){
         mpld3_load_lib("{{ mpld3_url }}", function(){
                 {{ extra_js }}
                 mpld3.draw_figure({{ figid }}, mpld3_data);
            })
         });
}

function showButtons() {
  toolbar.selectAll('image').transition(750).attr("y", 0);
}
function hideButtons() {
  toolbar.selectAll('image').transition(750).attr("y", 16);
}

mfigure = d3.selectAll(".mpld3-figure")
  .on("mouseenter", showButtons)
  .on("mouseleave", showButtons)
  .on("touchenter", showButtons)
  .on("touchstart", showButtons)
  .style('max-width,1040')
  .style('float','left')
toolbar = d3.selectAll(".mpld3-toolbar").attr("y", mfigure.attr('height')/2)  

pt0 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ])
pt1 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ])
m0 = new L.Marker([ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ]);
m1 = new L.Marker([ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ]);
map.addLayer(m0)
map.addLayer(m1)

map.fitBounds([
    [ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ],
    [ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ]
  ])

{{draw_js}}

map.on('dragend', function() {
  var po = map.getPixelOrigin(),
      pb = map.getPixelBounds(),
      offset = map.getPixelOrigin().subtract(map.getPixelBounds().min);
 background.style("left", -100-offset.x).style('top',-100-offset.y);
})

map.on('zoomend', function() {
  pt0 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[0],mdata.axes[0].xdomain[0] ])
  pt1 = map.latLngToLayerPoint([ mdata.axes[0].ydomain[1],mdata.axes[0].xdomain[1] ])
  mheight = pt0.y-pt1.y
  mwidth = pt1.x-pt0.x

  svg.attr("width", mwidth).attr("height", mheight).style("left",pt0.x+'px').style("top",pt1.y+'px')

  g2.attr('transform','translate('+ -svg.node().offsetLeft+','+ -svg.node().offsetTop+')')
  g2.selectAll('.line')
    .attr("d", ppath)
  g2.selectAll('.path')
    .attr("d", pathpath)
  g2.selectAll("circle")
    .attr("cx", function (d) { return map.latLngToLayerPoint(d.latLng).x;})
    .attr("cy", function (d) { return map.latLngToLayerPoint(d.latLng).y;})
});

map.zoomIn()
</script>
""")

def plotWithMap(fig,tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg", **kwargs):
  d3_url = urls.D3_LOCAL
  mpld3_url = urls.MPLD3_LOCAL
  # d3_url, mpld3_url = write_ipynb_local_js()

  figid = 'fig_' + get_id(fig) + str(int(random.random() * 1E10))

  renderer = MPLD3Renderer()
  Exporter(renderer, close_mpl=True).run(fig)

  fig, figure_json, extra_css, extra_js = renderer.finished_figures[0]

  extra_css = ""
  extra_js = ""
  with open(os.path.join(os.path.dirname(mpld3.__file__), 'js/d3.v3.min.js'),'r') as f:
    d3_js = f.read()
  with open(os.path.join(os.path.dirname(mpld3.__file__), 'js/mpld3.v0.2.js'),'r') as f:
    mpld3_js = f.read()
  with open(os.path.join(os.path.dirname(__file__), 'draw.js'),'r') as f:
    draw_js = f.read()
  with open(os.path.join(os.path.dirname(__file__), 'pyLeaflet.css'),'r') as f:
    pyLeaflet_css = f.read()

  # print json.dumps(figure_json)

  leaflet_init_js = """
    var width = 1040,
    height = 640;

    var mouseLat = 37;
    var mouseLng = -90;


    /*******************************************************************************
    *
    * Initialize map layout
    *
    *******************************************************************************/
    var map = L.map('map').setView([mouseLat, mouseLng],4);
    //map.scrollWheelZoom.disable();

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
    var ppath = d3.geo.path().projection(transform);

    var background = d3.select(map.getPanes().overlayPane)
        .insert("svg")
        .attr('width',width+200+'px')
        .attr('height',height+200+'px')
    background.append('rect')
      .attr('width',width+200+'px')
      .attr('height',height+200+'px')
      .style('fill','white')
      .style('fill-opacity',.6)

    var svg = d3.select(map.getPanes().overlayPane).append('svg').attr('width',5000).attr('height',3000);
    var g2   = svg.append('g').attr('class', 'leaflet-zoom-hide');

    """%(tile_layer)
  # tile_layer = "http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png"
  # tile_layer = "http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"
  # tile_layer = "http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.jpg"

  kwargs['mpld3_url'] = os.path.dirname(mpld3.__file__)+'/js/mpld3.js'
  kwargs['d3_url'] = os.path.dirname(mpld3.__file__)+'/js/d3.js'
  files = {os.path.dirname(mpld3.__file__)+'/js/mpld3.js': ["text/javascript",
                         open(urls.MPLD3_LOCAL, 'r').read()],
           os.path.dirname(mpld3.__file__)+'/js/d3.js': ["text/javascript",
                      open(urls.D3_LOCAL, 'r').read()]}

  html = MAP_HTML.render(figid=json.dumps(figid),
                         d3_url=d3_url,
                         mpld3_url=mpld3_url,
                         d3_js=d3_js,
                         mpld3_js=mpld3_js,
                         draw_js=draw_js,
                         figure_json=json.dumps(figure_json),
                         extra_css=extra_css,
                         extra_js=extra_js,
                         pyLeaflet_css=pyLeaflet_css,
                         leaflet_init_js=leaflet_init_js,
                         tile_layer=tile_layer)

  serve_and_open(html, ip='localhost', port=8888, n_retries=50, files=files)
  return html