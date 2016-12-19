all: build/spinel-composition.pdf build/fe-mg.pdf \
	build/corrected-spinels.tex

build:
	mkdir -p $@

build/spinel-composition.pdf: spinel-cr.py | build
	python $^ $@

build/corrected-spinels.tex: spinel-table.py | build
	python $^ $@

build/fe-mg.pdf: fe-mg.py | build
	python $^ $@
