OUT=build/ca-opx-pressures.pdf

all: $(OUT)

build:
	mkdir -p $@

$(OUT): make-figure.py | build
	python $^ $@

