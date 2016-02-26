all: build/cooling-scenarios.pdf build/timeline.pdf

build:
	mkdir -p $@

comparison: | build
	coffee comparison
	cairosvg -o build/comparison.pdf -d 100 build/comparison.svg

build/cooling-scenarios.pdf: scripts | build
	coffee $^
	cairosvg -o $@  -d 100 $(@:.pdf=.svg)

build/timeline.pdf: timeline | build
	coffee $^
	cairosvg -o $@ -d 100 $(@:.pdf=.svg)

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
