scenario:=fractional-melting
figure:=output/$(scenario).pdf
latex=output/depletion_degrees.tex


all: $(figure) output/depletion-model.pdf \
							 $(latex) | output
output:
	mkdir -p $@

table:=$(figure:.pdf=.tbl)
$(table): fractional-melting.melts-env
	cd $(dir $@) ;\
	run_alphamelts.command -f ../$^ -b ../fractional-melting.bat -o $(notdir $@);\
	rm -f *.txt

$(figure): clinopyroxene-depletion.py $(table)
	python $^ $@

scenario=clinopyroxene-depletion
figure=output/$(scenario).pdf
$(figure): $(scenario).py $(table)
	python $^ $@

output/depletion-model.pdf: make-model-plot.py $(table)
	python $^ $@

$(latex): depletion-degrees.py $(table)
	python $^ $@

