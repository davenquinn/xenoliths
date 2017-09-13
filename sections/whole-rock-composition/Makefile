all: build/major-elements.tex

build/major-elements.tex: major-elements.py templates/major-elements.tex
	mkdir -p $(dir $@)
	python $< major-elements.tex $@
