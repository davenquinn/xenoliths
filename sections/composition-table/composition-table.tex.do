#!/usr/bin/env zsh

deps=(header.tex
      ../mineral-compositions/minerals-partial.tex
      ../mineral-compositions/lava-minerals-partial.tex
      ../whole-rock-composition/major-elements-partial.tex
      footer.tex)

redo-ifchange $deps
cat $deps
