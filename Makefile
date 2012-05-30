all:
	convert artwork.jpg artwork.bmp
	potrace --svg artwork.bmp
	./svgtoscad.py artwork.bmp > artwork.scad
