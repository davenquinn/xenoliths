#!/usr/bin/env zsh

script=lava-minerals.py
template=templates/lava-minerals-partial.tex

redo-ifchange $script $template
python $script ${template:t} $3

