scenario:=fractional-melting
figure:=output/$(scenario).pdf
latex=output/depletion_degrees.tex


all: output/depletion-model.pdf \
			$(latex) output/ree-trends.pdf output/depletion-model-cpx.pdf | output
output:
	mkdir -p $@

table:=$(figure:.pdf=.tbl)
$(table): fractional-melting.melts-env
	cd $(dir $@) ;\
	run_alphamelts.command -f ../$^ -b ../fractional-melting.bat -o $(notdir $@);\
	rm -f *.txt

output/depletion-model.pdf: make-model-plot.py $(table)
	python $^ $@

output/depletion-model-cpx.pdf: make-model-plot.py $(table)
	python $< --clinopyroxene $(word 2,$^) $@

output/ree-trends.pdf: ree-trends.py $(table)
	python $^ $@

$(latex): depletion-degrees.py $(table)
	python $^ $@

