all: output/ternary.pdf

output:
	@mkdir -p $@

output/ternary.svg: modal-mineralogy.py | output
	./$^

output/ternary.pdf: output/ternary.svg | output
	cairosvg -o $@ -d 100 -W 500 -H 500 $^

d3-ternary:
	git submodule update --init

node_modules: d3-ternary
	npm install
	ln -s $^ $@/$^
