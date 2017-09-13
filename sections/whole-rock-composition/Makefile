all: prepare major_elements

prepare:
	mkdir -p build

major_elements: major-elements.py templates/major-elements.tex
	python major-elements.py
