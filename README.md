SCADTrace
=========

This is a toolset to convert a black-and-white bitmap into an
openscad object suitable for using to emboss a cylindrical object.

from something like this (image by Biofarben GmbH):

![Source Image](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork.jpg)

to this:

![Geometry](https://raw.githubusercontent.com/guyc/scadtrace/master/artwork-projected2.png)

It uses [potrace](http://potrace.sourceforge.net/) to generate an SVG representation of the figure from a bitmap.  potrace rocks.  
It then uses a python script to parse the SVG, extract the path geometry and generate openscad geometry.

Generating the inner and outer faces of the geometry presents a somewhat complicated
problem because the faces need to be expressed as triangles.
I've used [Triangle](http://www.cs.cmu.edu/~quake/triangle.html) to generate
tesselations, and it works well.  There are still some issues remaining
and the code is far from clean.

Dependencies
------------
 1. [potrace 1.11](http://potrace.sourceforge.net/) to generate an SVG representation of the figure from a bitmap.
 2. [triangle](http://www.cs.cmu.edu/~quake/triangle.html) to tesselate the SVG shapes into triangles.

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

Installation of potrace
-----------------------
Under OSX Mavericks, the steps are:
 1. wget http://potrace.sourceforge.net/download/potrace-1.11.tar.gz
 2. tar -zxf potrace-1.11.tar.gz
 3. cd potrace-1.11
 4. ./configure
 5. make
 6. sudo make install

Installation of Triangle
------------------------
Under OSX Mavericks the steps are:
 1. wget http://www.netlib.org/voronoi/triangle.zip
 2. unzip triangle.zip
 3. vi makefile
 4. Delete '-DLINUX' from the makefile
 5. make triangle

