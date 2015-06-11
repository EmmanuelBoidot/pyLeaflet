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

var lines   = {type:'FeatureCollection',features:[]}
var markers = {type:'FeatureCollection',features:[]}
var paths   = {type:'FeatureCollection',features:[]}
mdata.axes.forEach(function(a){
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
            }
        }
        mdata[l.coordinates][l.data].forEach(function(d){
            latlng = L.latLng(d[l.yindex], d[l.xindex])
            line.geometry.coordinates.push([d[l.yindex], d[l.xindex]])
        })
        lines.features.push(line)
    })
    a.markers.forEach(function(m){
        mdata[m.coordinates][m.data].forEach(function(d){
            marker = {
                id: m.id,
                type:'Feature',
                latLng: L.latLng(d[m.yindex], d[m.xindex]),
                properties:{
                    edgewidth:m.edgewidth,
                    edgecolor:m.edgecolor,
                    facecolor:m.facecolor,
                    alpha:m.alpha,
                    markertype:'circle',
                    radius:m.markerpath[0][0][1]
                }
            }
            markers.features.push(marker)
        })
    })
    a.paths.forEach(function(p){
        mpath = {
            id: p.id,
            type:'Feature',
            geometry:{
                type:'LineString',
                coordinates:[]
            },
            properties:{
                edgewidth:p.edgewidth,
                edgecolor:p.edgecolor,
                facecolor:p.facecolor,
                alpha:p.alpha,
            }
        }
        mdata[p.coordinates][p.data].forEach(function(d){
            latlng = L.latLng(d[p.yindex], d[p.xindex])
            mpath.geometry.coordinates.push([d[l.yindex], d[l.xindex]])
        })
        paths.features.push(mpath)
    })
})

d3lines = g2.selectAll('path')
    .data(lines.features)
    .enter()
    .append("path")
d3lines
    .attr("d", linepath)
    .attr('stroke', function(d){return d.properties.color})
    .attr('stroke-width', function(d){return d.properties.width})
    .attr("stroke-opacity", function(d){return d.properties.alpha})
    .style('fill', 'none');


d3markers = g2.selectAll(".marker")
    .data(markers.features).enter()
    .append('circle')
d3markers
    .attr('class','marker')
    .attr("cx", function (d) { return map.latLngToLayerPoint(d.latLng).x;})
    .attr("cy", function (d) { return map.latLngToLayerPoint(d.latLng).y;})
    .attr("r", function (d) { return d.properties.radius+"px";})
    .style("fill-opacity", function(d){return d.alpha})
    .style("fill", function(d){return d.facecolor})


