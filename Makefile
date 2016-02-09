all: comparison scenarios

build:
	mkdir -p $@

comparison: | build
	./generate-figure.py comparison
	cairosvg -o build/comparison.pdf -d 100 build/comparison.svg

scenarios: | build
	./generate-figure.py scripts
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
