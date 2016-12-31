all: build build/isotope-data.pdf build/isotope-data.tex build/isotope-table.pdf

build:
	mkdir -p $@

build/isotope-data.tex: generate-table.py
	python $^ $@

build/isotope-table.tex: build/isotope-data.tex
	cat $^ | paper standalone-table --landscape > $@

build/isotope-table.pdf: build/isotope-table.tex
	-xelatex -interaction=nonstopmode -output-directory build $^

build/isotope-data.pdf: generate-figure.py
	python $^ $@
