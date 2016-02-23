SCENARIOS = build/cooling-scenarios.pdf
TIMELINE = build/timeline.pdf

all: $(SCENARIOS) $(TIMELINE)

build:
	mkdir -p $@

comparison: | build
	coffee comparison
	cairosvg -o build/comparison.pdf -d 100 build/comparison.svg

$(SCENARIOS): scripts | build
	coffee $^
	cairosvg -o $@  -d 100 $(@:.pdf=.svg)



INT = $(TIMELINE:.pdf=.svg)
$(INT): timeline | build
	coffee $^
$(TIMELINE): $(INT)
	cairosvg -o $@ $^

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
