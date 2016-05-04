all: build/cooling-scenarios.pdf build/timeline.pdf build/comparison.pdf

build:
	mkdir -p $@

build/comparison.svg: comparison/index.coffee | build
	coffee $^ $@

build/comparison.pdf: build/comparison.svg
	sed -i -- 's/textpath/textPath/g' $^
	cairosvg -o $@ -d 72 $^

build/cooling-scenarios.pdf: time-slices | build
	coffee $^
	cairosvg -o $@  -d 100 $(@:.pdf=.svg)

build/timeline.pdf: timeline | build
	coffee $^
	cairosvg -o $@ -d 72 $(@:.pdf=.svg)

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
