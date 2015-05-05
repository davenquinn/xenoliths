all: figure greyscale
figure:
	mkdir -p build
	./generate-figure.py
	cairosvg -o build/cooling-scenarios.pdf -d 100 build/cooling-scenarios.svg
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
