all: build/isotope-data.pdf build/isotope-data.tex

build:
	mkdir -p $@

build/isotope-data.tex: generate-table.py | build
	python $^ $@

build/isotope-data.pdf: generate-figure.py | build
	python $^ $@
