#!/usr/bin/env zsh

redo-ifchange summary/temperature-summary.json summary/depletion-summary.json

pdf-printer --show --dpi 96 summary $3 >&2
