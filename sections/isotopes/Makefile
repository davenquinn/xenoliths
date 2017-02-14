all: build build/isotope-data.pdf build/isotope-data.tex build/isotope-table.pdf

build:
	mkdir -p $@

build/isotope-data.tex: generate-table.py
	python $^ $@

build/isotope-table.pdf: build/isotope-data.tex
	create-standalone-table $^ $@

build/isotope-data.pdf: generate-figure.py
	python $^ $@
