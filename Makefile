summary=build/temp-summary.pdf

all: build/pyx-dree.pdf build/temperatures.tex \
	build/temp-comparisons.pdf build/ree-temperatures.pdf \
	$(summary)

build:
	mkdir -p $@

build/data.pickle: get-data.py | build
	python $^

build/temp-comparisons.pdf: temp-comparisons.py
	python $^

build/ree-temperatures.pdf: ree-temperatures.py | build/data.pickle
	python $^

build/temperatures.tex: generate-table.py | build/data.pickle
	python $^

build/comparison-data.pickle: | build
	rm -f $@

build/pyx-dree.pdf: pyx-dree.py build/comparison-data.pickle | build
	python $<

svg=$(summary:.pdf=.svg)
$(svg): summary
	python summary-data.py | coffee $^ $@
$(summary): $(svg)
	cairosvg -o $@ -d 72 $^
