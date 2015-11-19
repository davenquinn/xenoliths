all: build/pyx-dree.pdf build/temperatures.tex

build:
	mkdir -p $@

build/temperatures.tex: generate-table.py | build
	python $^

build/pyx-dree.pdf: pyx-dree.py | build
	python $^

build/data.pickle: get-data.py | build
	python $^
