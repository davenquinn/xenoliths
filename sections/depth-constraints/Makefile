OUT=build/ca-ol-pressures.pdf

all: $(OUT)

build:
	mkdir -p $@

build/data.pickle: get-data.py | build
	python $^ $@

xa=build/xenoliths-area.json

$(xa): xenoliths-area.coffee 

$(OUT): make-figure.py build/data.pickle | build
	python $^ $@

