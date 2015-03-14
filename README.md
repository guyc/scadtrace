SCADTrace
=========

This is a toolset to convert a black-and-white bitmap into an
openscad object suitable for using to emboss a cylindrical object.

It uses [potrace](http://potrace.sourceforge.net/) to generate an SVG representation of the figure from a bitmap.  potrace rocks.  
It then uses a python script to parse the SVG, extract the path geometry and generate openscad geometry.

from something like this (image by Biofarben GmbH):

![Source Image](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork.jpg)

to this:

![Geometry](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork-projected.png)

Dependencies
------------
 1. [potrace 1.11](http://potrace.sourceforge.net/) to generate an SVG representation of the figure from a bitmap.
 2. [triangle](http://www.cs.cmu.edu/~quake/triangle.html) to tesselate the SVG shapes into triangles.

Update
------

Generating the inner and outer faces of the geometry presents a somewhat complicated
problem because the face needs to be expressed as triangles.
I've used [Triangle](http://www.cs.cmu.edu/~quake/triangle.html) to generate
tesselations, and it works well.  There are still some issues remaining
and the code is far from clean.

![Geometry](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork-projected2.png)

Note that we need to ensure that the triangle faces are small enough to wrap
around the outside of the cylinder.  So far using the "quality" setting on
triangle is giving me suitably small triangles, but I expect with large simple
shapes this may need more work.

Holes are not yet directly supported but you should be able to create separate positive
and negative geometry and use CSG to punch the holes.

Tesselations
------------
Here's a close-up that shows the effect of the triangulation.  Pretty, hey?
![Quality Tesselation](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork-tesselated.png)

The "quality" option introduces internal nodes which allow the geometry to
be deformed into a cylinder without nasty distortion of the faces.

![Quality Tesselation Projected](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork-tesselated-projected.png)

Here's the artwork used as a negative geometry to emboss the inside of a
translucent diffuser.

![Translucent Embossed Diffuser](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork-embossed-lens.png)

