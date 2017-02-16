#!/usr/bin/env zsh

(cd .. && pdf-printer spec.coffee >&2)
# Shim for weirdness of pdf-printer
mv ca-ol-pressures.temp.pdf $3
