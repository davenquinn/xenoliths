#!/usr/bin/env zsh

deps=(../make-figure.py data.pickle)
redo-ifchange $deps
python $deps $1 >&2