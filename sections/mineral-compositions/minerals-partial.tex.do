#!/usr/bin/env zsh

script=minerals.py
template=templates/minerals-partial.tex

redo-ifchange $script $template
python $script ${template:t} $3
