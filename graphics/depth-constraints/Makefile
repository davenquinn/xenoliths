OUT=build/ca-ol-pressures.pdf

all: $(OUT)

build:
	mkdir -p $@

build/data.pickle: get-data.py | build
	python $^ $@

$(OUT): make-figure.py build/data.pickle | build
	python $^ $@

