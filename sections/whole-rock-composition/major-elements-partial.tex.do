#!/usr/bin/env zsh

script=major-elements.py
template=templates/major-elements-partial.tex

redo-ifchange $script $template
python $script ${template:t} $3

