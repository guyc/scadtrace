all:
	convert artwork.jpg artwork.bmp
	potrace --svg artwork.bmp
	./svgtoscad.py artwork.svg

tri:
	~/src/triangle/triangle -p A.poly
