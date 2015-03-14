# set CONVERT to the location of the imagemagick convert binary
# see: http://www.imagemagick.org/
CONVERT = convert

# set TRIANGLE to the binary for quake triangle
# see: http://www.cs.cmu.edu/~quake/triangle.html
TRIANGLE = triangle/triangle

# set POTRACE to the binary for potrace
# see: http://potrace.sourceforge.net/
POTRACE = potrace/potrace-1.11/src/potrace

.PHONY: all bmp svg scad

all:	bmp svg scad

bmp:
	$(CONVERT) artwork.jpg artwork.bmp

svg:
	$(POTRACE) --svg artwork.bmp

scad:
	./svgtoscad.py --triangle $(TRIANGLE) --angle=60 --rotate artwork.svg
