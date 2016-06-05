scenario=fractional-melting
figure=output/$(scenario).pdf

all: $(figure) output/depletion-degrees.pdf | output

output:
	mkdir -p $@

table:=$(figure:.pdf=.tbl)
$(table): $(scenario).melts-env
	cd $(dir $@) ;\
	run_alphamelts.command -f ../$^ -b ../$(scenario).bat -o $(notdir $@);\
	rm -f *.txt

scenario=clinopyroxene-depletion
figure=output/$(scenario).pdf
$(figure): $(scenario).py $(table)
	python $^ $@

output/depletion-degrees.pdf: fit-depletion-degrees.py $(table)
	python $^ $@
