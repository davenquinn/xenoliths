all: build/pyx-dree.pdf build/temperatures.tex temp_comparisons

build:
	mkdir -p $@

build/data.pickle: get-data.py | build
	python $^

.PHONY: temp_comparisons
temp_comparisons: temp-comparisons.py | build/data.pickle
	python $^

build/temperatures.tex: generate-table.py | build/data.pickle
	python $^

build/pyx-dree.pdf: pyx-dree.py | build
	python $^
