all: build build/isotope-data.pdf build/isotope-table.pdf

build:
	mkdir -p $@

build/isotope-data.tex: generate-table.py | templates/isotopes.tex
	python $^ $@

build/isotope-table.pdf: build/isotope-data.tex
	create-standalone-table $^ $@

build/isotope-data.pdf: generate-figure.py
	python $^ $@
