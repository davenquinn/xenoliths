#!/usr/bin/env zsh

deps=$PROJECT_DIR/versioned/sections/thermometry/temperature-summary.json
redo-ifchange $deps

cp $deps $3
