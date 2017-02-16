#!/usr/bin/env zsh

DEPS=../bin/get-data
echo $VIRTUAL_ENV >&2
redo-ifchange $DEPS
$VIRTUAL_ENV/bin/python $DEPS $3 >&2
