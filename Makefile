all: build/isotope-data.pdf

build:
	mkdir -p $@

table: generate-table.py | build
	python $^

build/isotope-data.pdf: generate-figure.py | build
	python $^ $@
