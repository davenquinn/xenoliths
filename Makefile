all: figure greyscale
figure:
	mkdir -p build
	./generate-figure.py
	rsvg-convert -f pdf -o build/cooling-scenarios.pdf build/cooling-scenarios.svg
greyscale:
	gs \
	 -sOutputFile=build/cooling-scenarios.greyscale.pdf \
	 -sDEVICE=pdfwrite \
	 -sColorConversionStrategy=Gray \
	 -dProcessColorModel=/DeviceGray \
	 -dCompatibilityLevel=1.4 \
	 -dNOPAUSE \
	 -dBATCH \
	 build/cooling-scenarios.pdf
