all: output/ternary.pdf

output:
	@mkdir -p $@

output/ternary.svg: modal-mineralogy.py | output
	./$^

output/ternary.pdf: output/ternary.svg | output
	cairosvg -o $@ -d 100 $^

node_modules:
	npm install
	npm link d3-ternary
