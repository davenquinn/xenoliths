all: build/pyx-dree.pdf build/temperatures.tex build/temp-comparisons.pdf build/ree-temperatures.pdf

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

build/pyx-dree.pdf: pyx-dree.py | build
	python $^

