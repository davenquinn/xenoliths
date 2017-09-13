all: build/minerals.tex build/lava_minerals.tex | build

build:
	mkdir -p $@

build/minerals.tex: generate.py
	python $^

build/lava_minerals.tex: lava-minerals.py
	python $^ $@
