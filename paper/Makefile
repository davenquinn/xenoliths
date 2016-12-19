# Makefile

INFILE = main
AUXFILE = build/$(INFILE).aux

INFILE_D = draft
AUXFILE_D = build/$(INFILE_D).aux

PAPER_DIR=/Users/Daven/Resources/Papers

LIBRARY = $(PAPER_DIR)/bibtex/library.bib
BIBFILE = source/references.bib
BIBSTYLE = source/lib/agu.csl

out=output/Quinn-2016-xenoliths.pdf
doc=$(out:.pdf=.docx)

remote=$(PAPER_DIR)/Unpublished/$(notdir $(out))

all: $(out) $(doc) $(remote) | build output

build:
	mkdir -p $@

output:
	mkdir -p $@

build/body.tex: text/body.md text/includes.yaml $(wildcard collected/*.tex)
	paper create-body text $@

build/abstract.tex: text/abstract.md
	pandoc -t latex --natbib -o $@ $^

text=build/body.tex build/abstract.tex

build/main.aux: $(text)
source/main.tex: $(text)

citations: build/main.aux $(BIBFILE)
	echo "Updating Bibliograpy"
	-bibtex $<
	-bibtex $(AUXFILE_D)

collected:
	mkdir -p $@

.PHONY: includes
includes: text/includes.yaml | collected
	scripts/collect-figures

XELATEX = -xelatex -interaction=nonstopmode -output-directory build

$(out): source/main.tex citations includes
	$(XELATEX) $<
	mv build/main.pdf $@

draft: text citations
	cp build/body.tex build/body_draft.tex
	sed -i 's/{table\*}/{table}/g' build/body_draft.tex
	sed -i 's/{figure\*}/{figure}/g' build/body_draft.tex
	$(XELATEX) source/$(INFILE_D).tex
	mv build/draft.pdf output/draft.pdf

$(BIBFILE): build/main.aux $(LIBRARY)
	scripts/bib-filter/bib-filter --clean --aux $^ $@

build/figures.md: text/includes.yaml
	scripts/inline-figures $^ > $@

$(doc): text/abstract.md text/body.md build/figures.md
	pandoc -t docx --bibliography=$(BIBFILE) --csl=$(BIBSTYLE) -o $@ $^

$(remote): $(out)
	mkdir -p $(dir $@)
	ln -s $^ $@

