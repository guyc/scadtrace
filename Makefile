all:
	convert artwork.jpg artwork.bmp
	potrace --svg artwork.bmp
