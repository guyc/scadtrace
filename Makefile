.PHONY: all bmp svg scad

all:	bmp svg scad

bmp:
	convert artwork.jpg artwork.bmp

svg:
	potrace --svg artwork.bmp

scad:
	./svgtoscad.py artwork.svg
