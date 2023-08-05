hscquery
========
.. inclusion-marker-main-readme

Module for querying the *Hyper Suprime-Cam Subaru Strategic Program*
database. `HSC-SSP`_

Based on the python script developed by michitaro, NAOJ / HSC
Collaboration. `Source`_

Dependencies
------------

``hscquery`` depends on ``Astropy``

Installation
------------

``hscquery`` can be easily installed using ``pip``: 
``pip install hscquery``

|astropy|

.. _HSC-SSP: https://hsc.mtk.nao.ac.jp/ssp/
.. _Source: https://hsc-gitlab.mtk.nao.ac.jp/snippets/17

.. |astropy| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
   :target: http://www.astropy.org/

Example
-------
A simple example of using ``hscquery``::

    from hscquery import HSC
    from astropy import units as u
    from astropy.coordinates import SkyCoord
    
    coords = SkyCoord(34.0, -5.0, unit='deg')
    radius = 5.0 * u.arcsec
    
    h = HSC(survey='wide')
    data = h.query_region(coords, radius)
    print data