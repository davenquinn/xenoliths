#!/usr/bin/env zsh

redo-ifchange summary/temperature-summary.json

pdf-printer summary --show --wait $3 >&2
