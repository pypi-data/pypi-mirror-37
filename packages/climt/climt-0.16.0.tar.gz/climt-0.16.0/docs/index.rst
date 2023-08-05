Welcome to climt's documentation!
=================================

.. figure:: climt_logo.jpg
   :width: 1500px
   :height: 750px
   :scale: 50%
   :alt: climt logo
   :align: center

   Background: **Approaching Thunderstorm** (Gustav Klimt).
   
   Image source: `Wikimedia Commons`_ 


.. _Wikimedia Commons:
    https://commons.wikimedia.org/wiki/File:Gustav_Klimt_-_Approaching_Thunderstorm_(The_Large_Poplar_II)_-_Google_Art_Project.jpg


climt (Climate Modelling and Diagnostics Toolkit) is a Python based library which provides a
modular and intuitive approach to writing numerical models of the climate system. climt provides
state-of-the art components and an easy-to-use interface to allow writing research quality models
without the hassle of modifying Fortran code.

The modular nature of climt allows re-use of model code, allowing users to build progressively
complicated models without having to rewrite the same code at each level of complexity.

climt uses `sympl`_ for its modelling infrastructure, making climt components and model scripts highly readable
and self-documenting.

.. _sympl:
    https://sympl.readthedocs.io

Contents:

.. toctree::
   :maxdepth: 2

   introduction
   installation
   quickstart
   interaction
   realistic
   component_types
   configuration
   components
   initialisation
   utilities
   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
