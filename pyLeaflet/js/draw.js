var transform = ["", "-webkit-", "-moz-", "-ms-", "-o-"].reduce(function(p, v) { return v + "transform" in document.body.style ? v : p; }) + "transform";

var lineFunc = d3.svg.line()
    .x(function(d) {
      return map.latLngToLayerPoint(d.latLng).x;
    })
    .y(function(d) {
      return map.latLngToLayerPoint(d.latLng).y;
    })
    .interpolate('linear');

function project(point) {
    var latlng = new L.LatLng(point[1], point[0]);
    var layerPoint = map.latLngToLayerPoint(latlng);
    return [layerPoint.x, layerPoint.y];
} 
var linepath = d3.geo.path().projection(project);

function pathCollection(){
    return pyLeaflet.pyLeaflet_path().x(function(d) {
      pt = map.latLngToLayerPoint([ this.pathcoords.x(d[0]),this.pathcoords.y(d[1]) ]);
      return pt.x;
    }.bind(this)).y(function(d) {
      pt = map.latLngToLayerPoint([ this.pathcoords.x(d[0]),this.pathcoords.y(d[1]) ]);
      return pt.y;
    }.bind(this)).apply(this, pyLeaflet.getMod(this.props.paths, i));
}

function mypath(vertices, pathcodes) {
    var n_vertices = {
      M: 1,
      m: 1,
      L: 1,
      l: 1,
      Q: 2,
      q: 2,
      T: 1,
      t: 1,
      S: 2,
      s: 2,
      C: 3,
      c: 3,
      Z: 0,
      z: 0
    };
    var defined = function(d, i) {
      return true;
    };
    var points = [], segments = [], i_v = 0, i_c = -1, halt = 0, nullpath = false;
    if (!pathcodes) {
        pathcodes = [ "M" ];
        for (var i = 1; i < vertices.length; i++) pathcodes.push("L");
    }
    while (++i_c < pathcodes.length) {
        halt = i_v + n_vertices[pathcodes[i_c]];
        points = [];
        while (i_v < halt) {
          if (defined.call(this, vertices[i_v], i_v)) {
            points.push(vertices[i_v].x,vertices[i_v].y);
            i_v++;
          } else {
            points = null;
            i_v = halt;
          }
        }
        if (!points) {
          nullpath = true;
        } else if (nullpath && points.length > 0) {
          segments.push("M", points[0], points[1]);
          nullpath = false;
        } else {
          segments.push(pathcodes[i_c]);
          segments = segments.concat(points);
        }
    }
    if (i_v != vertices.length) console.warn("Warning: not all vertices used in Path");
    return segments.join(" ");
}

function pathpath(p){
    vertices = []; 
    p.geometry.coordinates.forEach(function(d){
        l=map.latLngToLayerPoint(d); 
        vertices.push(l)
    })
    return mypath(vertices, p.geometry.pathcodes)
}

function collectionpath(p){
    vertices = [];
    l = project(p.geometry.offsetcoordinates)
    p.geometry.coordinates.forEach(function(d){
        vertices.push({x:d[0]+l[0],y:d[1]+l[1]})
    })
    return mypath(vertices, p.geometry.pathcodes)
}

function displaypath(p){
    vertices = []; 
    p.geometry.coordinates.forEach(function(d){
        vertices.push({x:d[0],y:d[1]})
    })
    return mypath(vertices, p.geometry.pathcodes)
}

function collectionpath_transformFunc(d) {
    var t = d.properties.transform;
    var transform = t === undefined || t.length == 0 ? "" : d3.transform("matrix(" + t + ")").toString();
    var l = project(d.geometry.offsetcoordinates)
    var offset = d === null || typeof d === "undefined" ? "translate(0, 0)" : "translate(" + l[0]+','+ l[1] + ")";
    return offset+transform;
}

function displaypath_translate(d){
    l=map.latLngToLayerPoint(d.properties.translate); 
    return "translate("+l.x+","+l.y+")"
}


var lines           = {type:'FeatureCollection',features:[]};
var markers         = {type:'FeatureCollection',features:[]};
var markerpaths     = {type:'FeatureCollection',features:[]};
var paths           = {type:'FeatureCollection',features:[]};
var displaypaths    = {type:'FeatureCollection',features:[]};
var collectionpaths = {type:'FeatureCollection',features:[]};
mdata.axes.slice(0,1).forEach(function(a){
    a.collections.forEach(function(c){
        c.paths.forEach(function(p,i){
            mpath = {
                id: c.id+'path'+i,
                type:'Feature',
                geometry:{
                    type:'LineString',
                    coordinates:[],
                    pathcodes:p[1]
                },
                properties:{
                    edgewidth: (c.edgewidths.length>=i)?c.edgewidths[i]:c.edgewidths[0],
                    edgecolor: (c.edgecolors.length>=i)?c.edgecolors[i]:c.edgecolors[0],
                    facecolor: (c.facecolors.length>=i)?c.facecolors[i]:c.facecolors[0],
                    alpha: (c.alphas.length>=i)?c.alphas[i]:c.alphas[0],
                    zorder: c.zorder
                }
            }
            // means the path is actual signal
            if (c.coordinates == 'data' || c.pathcoordinates == 'data'){
                p[0].forEach(function(d){
                    mpath.geometry.coordinates.push([d[1],d[0]])
                })
                paths.features.push(mpath)
            // means the path is a symbol
            } else if (c.pathcoordinates == "display"){
                if (c.offsetcoordinates == "display"){
                    mpath.properties.translate = [mdata.data[c.offsets][i][1],mdata.data[c.offsets][i][0]];
                    p[0].forEach(function(d){
                        mpath.geometry.coordinates.push([d[0],d[1]])
                    })
                    displaypaths.features.push(mpath)
                } else if (c.offsetcoordinates == "data"){
                    mpath.properties.translate = [0,0]
                    mdata.data[c.offsets].forEach(function(o,j){
                        mpath = {
                            id: c.id+'path'+j,
                            type:'Feature',
                            geometry:{
                                type:'LineString',
                                coordinates:[],
                                offsetcoordinates:o,
                                pathcodes:p[1]
                            },
                            properties:{
                                edgewidth: (c.edgewidths.length>=j)?c.edgewidths[j]:c.edgewidths[0],
                                edgecolor: (c.edgecolors.length>=j)?c.edgecolors[j]:c.edgecolors[0],
                                facecolor: (c.facecolors.length>=j)?c.facecolors[j]:c.facecolors[0],
                                alpha: (c.alphas.length>=j)?c.alphas[j]:c.alphas[0],
                                translate: [0,0],
                                transform: c.pathtransforms[j],
                                zorder: c.zorder
                            }
                        }
                        p[0].forEach(function(d){
                            mpath.geometry.coordinates.push([d[0],d[1]])
                        })
                        collectionpaths.features.push(mpath)
                    })
                }
            }
        })
        a
    })

    a.lines.forEach(function(l){
        line = {
            id: l.id,
            type:'Feature',
            geometry:{
                type:'LineString',
                coordinates:[]
            },
            properties:{
                width:l.linewidth,
                color:l.color,
                alpha:l.alpha,
                dasharray:l.dasharray,
            }
        }
        mdata.data[l.data].forEach(function(d){
            line.geometry.coordinates.push([d[l.yindex], d[l.xindex]])
        })
        lines.features.push(line)
    })
    a.markers.forEach(function(m){
        mdata.data[m.data].forEach(function(d){
            // marker = {
            //     id: m.id,
            //     type:'Feature',
            //     latLng: L.latLng(d[m.yindex], d[m.xindex]),
            //     geometry:{
            //         type:'LineString',
            //         coordinates:[],
            //         pathcodes:m.pathcodes
            //     },
            //     properties:{
            //         edgewidth:m.edgewidth,
            //         edgecolor:m.edgecolor,
            //         facecolor:m.facecolor,
            //         alpha:m.alpha,
            //         markertype:'circle',
            //         radius:m.markerpath[0][0][1]
            //     }
            // }
            // markers.features.push(marker)

            mpath = {
                id: m.id,
                type:'Feature',
                geometry:{
                    type:'LineString',
                    offsetcoordinates:d,
                    coordinates:m.markerpath[0],
                    pathcodes:m.markerpath[1]
                },
                properties:{
                    edgewidth:m.edgewidth,
                    edgecolor:m.edgecolor,
                    facecolor:m.facecolor,
                    alpha:m.alpha,
                    dasharray:m.dasharray,
                    zorder:m.zorder,
                }
            }
            markerpaths.features.push(mpath)
        })
    })
    a.paths.forEach(function(p){
        mpath = {
            id: p.id,
            type:'Feature',
            geometry:{
                type:'LineString',
                coordinates:[],
                pathcodes:p.pathcodes
            },
            properties:{
                edgewidth:p.edgewidth,
                edgecolor:p.edgecolor,
                facecolor:p.facecolor,
                alpha:p.alpha,
                dasharray:p.dasharray,
                zorder: p.zorder
            }
        }
        mdata.data[p.data].forEach(function(d){
            mpath.geometry.coordinates.push([d[p.yindex], d[p.xindex]])
        })
        paths.features.push(mpath)
    })
})

d3lines = g2.selectAll('.line')
    .data(lines.features)
    .enter()
    .append("path");
d3lines
    .attr("d", linepath)
    .attr('class','line')
    .attr('stroke', function(d){return d.properties.color})
    .attr('stroke-width', function(d){return d.properties.width})
    .attr("stroke-opacity", function(d){return d.properties.alpha})
    .attr("stroke-dasharray", function(d){return d.properties.dasharray})
    .attr("vector-effect","non-scaling-stroke")
    .style('z-index', function(d){return d.properties.zorder})
    .style('fill', 'none')
    .attr('id', function(d){return d.id});


// d3markers = g2.selectAll(".marker")
//     .data(markers.features).enter()
//     .append('circle');
// d3markers
//     .attr('class', function(d){return 'marker marker-'+d.id})
//     .attr("cx", function (d) { return map.latLngToLayerPoint(d.latLng).x;})
//     .attr("cy", function (d) { return map.latLngToLayerPoint(d.latLng).y;})
//     .attr("r", function (d) { return d.properties.radius+"px";})
//     .attr("fill-opacity", function(d){return d.properties.alpha})
//     .attr("fill", function(d){return d.properties.facecolor});

d3markerpaths = g2.selectAll('.markerpath')
    .data(markerpaths.features)
    .enter()
    .append("path");
d3markerpaths
    .attr("d", displaypath)
    .attr('class','markerpath')
    .attr('stroke', function(d){return d.properties.edgecolor})
    .attr('stroke-width', function(d){return d.properties.edgewidth})
    .attr("stroke-opacity", function(d){return d.properties.alpha})
    .attr("transform", collectionpath_transformFunc)
    .attr("vector-effect","non-scaling-stroke")
    // .style(transform, function(d){ return "matrix3d("+d.properties.transform + ")";})
    .style('fill', function(d){return d.properties.facecolor})
    .style('fill-opacity', function(d){return d.properties.alpha})
    .style('z-index', function(d){return d.properties.zorder})
    .attr('id', function(d){return d.id});

d3paths = g2.selectAll('.path')
    .data(paths.features)
    .enter()
    .append("path");
d3paths
    .attr("d", pathpath )
    .attr('class','path')
    .attr('stroke', function(d){return d.properties.edgecolor})
    .attr('stroke-width', function(d){return d.properties.edgewidth})
    .attr("stroke-opacity", function(d){return d.properties.alpha})
    .attr("stroke-dasharray", function(d){return d.properties.dasharray})
    .style('fill', function(d){return d.properties.facecolor})
    .style('fill-opacity', function(d){return d.properties.alpha})
    .style('z-index', function(d){return d.properties.zorder})
    .attr("vector-effect","non-scaling-stroke")
    .attr('id', function(d){return d.id});

d3displaypaths = g2.selectAll('.displaypath')
    .data(displaypaths.features)
    .enter()
    .append("path");
d3displaypaths
    .attr("d", displaypath)
    .attr('class','displaypath')
    .attr('stroke', function(d){return d.properties.edgecolor})
    .attr('stroke-width', function(d){return d.properties.edgewidth})
    .attr("stroke-opacity", function(d){return d.properties.alpha})
    .attr("transform", displaypath_translate)
    .style('fill', function(d){return d.properties.facecolor})
    .style('fill-opacity', function(d){return d.properties.alpha})
    .style('z-index', function(d){return d.properties.zorder})
    .attr("vector-effect","non-scaling-stroke")
    .attr('id', function(d){return d.id});

d3collectionpaths = g2.selectAll('.collectionpath')
    .data(collectionpaths.features)
    .enter()
    .append("path");
d3collectionpaths
    .attr("d", displaypath)
    .attr('class','collectionpath')
    .attr('stroke', function(d){return d.properties.edgecolor})
    .attr('stroke-width', function(d){return d.properties.edgewidth})
    .attr("stroke-opacity", function(d){return d.properties.alpha})
    .attr("transform", collectionpath_transformFunc)
    .attr("vector-effect","non-scaling-stroke")
    // .style(transform, function(d){ return "matrix3d("+d.properties.transform + ")";})
    .style('fill', function(d){return d.properties.facecolor})
    .style('fill-opacity', function(d){return d.properties.alpha})
    .style('z-index', function(d){return d.properties.zorder})
    .attr('id', function(d){return d.id});

g2.selectAll('.line')
    .attr("d", ppath);

