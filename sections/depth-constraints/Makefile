OUT=build/ca-ol-pressures.pdf
OUT2=build/heatflow-comparison.pdf

all: $(OUT) $(OUT2) | build

build:
	mkdir -p $@

build/data.pickle: get-data.py | build
	python $^ $@

xa=build/xenoliths-area.json

$(xa): xenoliths-area.coffee 

$(OUT): make-figure.py build/data.pickle
	python $^ $@

$(OUT2): heatflow-comparison.py
	python $^ $@

