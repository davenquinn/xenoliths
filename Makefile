scenario=fractional-melting
figure=output/$(scenario).pdf

all: $(figure) | output

output:
	mkdir -p $@

table=$(figure:.pdf=.tbl)
$(table): $(scenario).melts-env
	cd $(dir $@) ;\
	run_alphamelts.command -f ../$^ -b ../$(scenario).bat -o $(notdir $@);\
	rm -f *.txt

$(figure): $(scenario).py $(table)
	python $^ $@
