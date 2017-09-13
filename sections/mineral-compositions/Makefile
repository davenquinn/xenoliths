all: build/minerals.tex build/lava_minerals.tex | build

build:
	mkdir -p $@

build/minerals.tex: minerals.py
	python $^ $(notdir $@) $@

build/lava_minerals.tex: lava-minerals.py
	python $^ $(notdir $@) $@
