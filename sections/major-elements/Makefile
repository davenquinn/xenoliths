all: build/spinel-composition.pdf build/fe-mg.pdf \
	build/corrected-spinels-table.pdf

build:
	mkdir -p $@

build/spinel-composition.pdf: spinel-cr.py spinel_calc.py | build
	python $< $@

build/corrected-spinels.tex: spinel-table.py spinel_calc.py templates/corrected-spinels.tex | build
	python $< $@

build/corrected-spinels-table.pdf: build/corrected-spinels.tex
	create-standalone-table $^ $@

build/fe-mg.pdf: fe-mg.py | build
	python $^ $@
