cs=build/cooling-scenarios.pdf

all: $(cs) build/timeline.pdf build/comparison.pdf

build:
	mkdir -p $@

build/comparison.svg: comparison/index.coffee | build
	coffee $^ $@

build/comparison.pdf: build/comparison.svg
	sed -i -- 's/textpath/textPath/g' $^
	sed -i -- 's/textarea/textArea/g' $^
	cairosvg -o $@ -d 72 $^

_cs=$(cs:.pdf=.svg)
$(_cs): time-slices | build
	coffee $^ $@

$(cs): $(_cs)
	cairosvg -o $@  -d 100 $^

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
