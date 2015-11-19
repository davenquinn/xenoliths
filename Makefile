all: build/trace-elements.tex \
	build/trace-elements.pdf \
	build/enrichment.pdf

build:
	mkdir -p $@

build/enrichment.pdf: enrichment-trends.py | build
	python $^

build/trace-elements.tex: generate-table.py | build
	python $^

build/trace-elements.pdf: generate-figure.py | build
	python $^
