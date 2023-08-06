.. Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

PISM-Palseries
==============

A small script to prepare scalar modifier temperature and precipitation time
series for the Parallel Ice Sheet Model (PISM_) based on online-available
palaeo-climate records or simple mathematical functions.

Requires NetCDF4_ and Numpy_.

Installation::

   pip install pism-palseries

Example usage::

   pism_palseries.py ramp 0 1000 0 -10 --output ramp.nc
   pism_palseries.py --help

.. _NetCDF4: https://unidata.github.io/netcdf4-python/
.. _Numpy: https://www.numpy.org/
.. _PISM: http://pism-docs.org/
