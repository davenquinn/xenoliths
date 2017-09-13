scenario:=fractional-melting
figure:=output/$(scenario).pdf
latex=output/depletion_degrees.tex
depletion_data=output/depletion-data.json

all: output/depletion-model.pdf \
			$(latex) output/ree-trends.pdf \
			output/PT-plot.pdf \
			output/depletion-model-cpx.pdf \
			$(depletion_data) | output
output:
	mkdir -p $@

table:=$(figure:.pdf=.tbl)
$(table): fractional-melting.melts-env literature/WH_oDMM_REE-x.melts
	cd $(dir $@) ;\
	run_alphamelts.command -f ../$< -b ../fractional-melting.bat -o $(notdir $@);\
	rm -f *.txt

output/depletion-model.pdf: make-model-plot.py $(table)
	python $^ $@

output/depletion-model-cpx.pdf: make-model-plot.py $(table)
	python $< --clinopyroxene $(word 2,$^) $@

output/ree-trends.pdf: ree_trends.py $(table)
	python $^ $@

output/PT-plot.pdf: make-pt-plot.py $(table)
	python $^ $@

$(latex): depletion-degrees.py $(table)
	python $^ $@

$(depletion_data): depletion-degrees-data.py $(table)
	python $^ $@
