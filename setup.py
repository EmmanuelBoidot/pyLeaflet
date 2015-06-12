#!/usr/bin/env python

from distutils.core import setup

setup(name='pyLeaflet',
      version='1.0',
      description='mpld3 extension for plotting data on a Leaflet map',
      author='Emmanuel Boidot',
      author_email='emmanuel.boidot@gmail.com',
      url='https://github.com/EmmanuelBoidot/pyLeaflet',
      packages=['pyLeaflet'],
      package_dir = {'pyLeaflet': 'pyLeaflet'},
      package_data={'pyLeaflet': ['draw.js','pyLeaflet.css']}
     )