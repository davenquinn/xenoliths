#!/usr/bin/env zsh

deps=$PROJECT_DIR/versioned/sections/major-elements/build/spinel-data.json
redo-ifchange $deps

cp $deps $3

