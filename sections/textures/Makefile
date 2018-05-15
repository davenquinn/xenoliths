all: build/textures.pdf

build:
	mkdir -p $@

#build/classes.json: make-textures.py | build
#	python $^

build/textures.svg: build/classes.json | build
	coffee generate/index.coffee

build/textures.pdf: build/textures.svg
	cairosvg -o $@ -d 72 $^
