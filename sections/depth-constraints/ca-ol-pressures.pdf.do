#!/usr/bin/env zsh

redo-ifchange add-xenoliths-area/* build/ca-ol-pressures.svg
pdf-printer add-xenoliths-area $3 >&2
