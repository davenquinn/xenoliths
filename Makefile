all: fractional-melting | output

output:
	mkdir -p $@

output/fractional-melting.tbl: fractional-melting.melts-env
	cd $(dir @) ;\
	run_alphamelts.command -f ../$^ -b ../$(notdir @).bat -o $(notdir @).tbl

.PHONY: fractional-melting
fractional-melting: fractional-melting.py output/fractional-melting.tbl
	python $^
