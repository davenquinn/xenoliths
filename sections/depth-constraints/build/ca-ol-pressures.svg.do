#!/usr/bin/env zsh

deps=(../make-figure.py data.pickle)
redo-ifchange $deps
$VIRTUAL_ENV/bin/python $deps $1 >&2
