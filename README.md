# pyLeaflet
mpld3 extension for plotting data on a Leaflet map

About
-----
pyLeaflet it an extension of mpld3 that provides geolocalized data visualization on a Leaflet layer as an overlay pane.


Installation
------------
pyLeaflet is compatible with python 2.6-2.7 (python 3 not tested). It requires
[mpld3](http://mpld3.github.io),
[matplotlib](http://matplotlib.org) version 1.3 and
[jinja2](http://jinja.pocoo.org/) version 2.7+.

To install:
- clone project

     [~]$ git clone https://github.com/EmmanuelBoidot/pyLeaflet.git

- within the git source directory, run

     [~]$ python setup.py install

Example Plot
----------
An example script is provided in this project: see ``example.py''. In order to plot geodata using pyLeaflet, proceed as for MatPlotLib, using the longitude as the first coordinate and the latitude as the second coordinate.

Next
----
- brush selector for timeseries display on the map
- animations (not supported by mpld3)