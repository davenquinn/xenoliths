all: build/trace-elements.tex build/trace-elements.pdf

build:
	mkdir -p $@

build/trace-elements.tex: generate-table.py | build
	python $^

build/trace-elements.pdf: generate-figure.py | build
	python $^
