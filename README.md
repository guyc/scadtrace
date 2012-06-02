SCADTrace
=========

This is a toolset to convert a black-and-white bitmap into an
openscad object suitable for using to emboss a cylindrical object.

It uses [potrace](http://potrace.sourceforge.net/) to generate an SVG representation of the figure from a bitmap.  potrace rocks.  
It then uses a python script to parse the SVG, extract the path geometry and generate openscad geometry.

from something like this (image by Biofarben GmbH):

![Source Image](scadtrace/raw/master/artwork.jpg)

to this:

![Geometry](scadtrace/raw/master/artwork-projected.png)

Update
------

Generating the inner and outer faces of the geometry presents a somewhat complicated
problem because the face needs to be expressed as triangles.
I've used [Triangle](http://www.cs.cmu.edu/~quake/triangle.html) to generate
tesselations, and it works well.  There are still some issues remaining
and the code is far from clean.

![Geometry](scadtrace/raw/master/artwork-projected2.png)

Note that we need to ensure that the triangle faces are small enough to wrap
around the outside of the cylinder.  So far using the "quality" setting on
triangle is giving me suitably small triangles, but I expect with large simple
shapes this may need more work.

Holes are not yet directly supported but you should be able to create separate positive
and negative geometry and use CSG to punch the holes.

![Source Image](scadtrace/raw/master/artwork-tesselated.jpg)
