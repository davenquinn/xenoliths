all: output/cpx-profile.pdf

output:
	mkdir -p $@

output/cpx-profile.pdf: cpx-profile.py | output
	python $^ $@

