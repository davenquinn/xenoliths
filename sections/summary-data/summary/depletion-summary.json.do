#!/usr/bin/env zsh

deps=$PROJECT_DIR/versioned/sections/depletion-model/output/depletion-data.json
redo-ifchange $deps

cp $deps $3

