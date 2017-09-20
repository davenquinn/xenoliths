all: build/spinel-composition.pdf build/fe-mg.pdf \
	build/corrected-spinels-table.pdf \
	build/spinel-composition-with-uncorrected.pdf \
	build/spinel-data.json

build:
	mkdir -p $@

build/spinel-data.json: serialize-spinel-cr.py | build
	python $^ $@

DEPS=spinel-cr.py spinel_calc.py spinel-cr-annotations.yaml

build/spinel-composition-with-uncorrected.pdf: $(DEPS) | build
	PLOT_UNCORRECTED=1 python $< $@

build/spinel-composition.pdf: $(DEPS) | build
	python $< $@

build/corrected-spinels.tex: spinel-table.py spinel_calc.py templates/corrected-spinels.tex | build
	python $< $@

build/corrected-spinels-table.pdf: build/corrected-spinels.tex
	create-standalone-table $^ $@

build/fe-mg.pdf: fe-mg.py | build
	python $^ $@
