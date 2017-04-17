all: build/trace-elements.tex \
	build/trace-elements-table.pdf \
	build/trace-elements.pdf \
	build/cpx-opx-ratio.pdf \
	build/whole-rock.pdf \
	build/literature-comparison.pdf

build:
	mkdir -p $@

build/trace-elements-table.pdf: build/trace-elements.tex
	create-standalone-table $^ $@

build/trace-elements.tex: generate-table.py | build templates/trace-elements.tex
	python $^

build/trace-elements.pdf: generate-figure.py | build
	python $^

build/whole-rock.pdf: whole-rock.py | build
	python $^

build/cpx-opx-ratio.pdf: ratioed.py | build
	python $^ $@

build/literature-comparison.pdf: comparison.py | build
	python $^ $@
