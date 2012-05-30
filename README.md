SCADTrace
=========

This is a toolset to convert a black-and-white bitmap into an
openscad object suitable for using to emboss a cylindrical object.

It uses [potrace](http://potrace.sourceforge.net/) to generate an SVG representation of the figure from a bitmap.  potrace rocks.  
It then uses a python script to parse the SVG, extract the path geometry and generate openscad geometry.

from this:

![Source Image](scadtrace/raw/master/artwork.jpg)

to this:

![Geometry](scadtrace/raw/master/artwork-projected.png)

Work in Progress
----------------

The openscad geometry generated does not yet include the inner or outer faces.
OpenSCAD polyhedrons are expressed as triangles, so we need to tesselate the face polygons
before we can generate the face geometry.  I think the best solution will be to 
use [Triangle](http://www.cs.cmu.edu/~quake/triangle.html).

We also need to ensure that the triangle faces are small enough to wrap
around the outside of the cylinder, although that may fall out of triangle naturally.
Maybe we can specify a maximum size of the tesselation triangles?
