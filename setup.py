#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by Måns Magnusson on 2013-04-22.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from distutils.core import setup

setup(
    name="DLA_Genotyper",
    version="0.1dev",
packages={'DLA_Genotyper', 'DLA_Genotyper.utils', 'DLA_Genotyper.produce_plots'},
    package_dir={ "DLA_Genotyper" : "DLA_Genotyper" },
    license="Modified BSD",
    long_description = open( "README.md", "r" ).read( ),
    maintainer="Mans Magnusson",
    maintainer_email="mans.magnusson@scilifelab.se"
)
