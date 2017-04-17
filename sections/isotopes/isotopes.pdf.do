SCRIPT=generate-figure.py

redo-ifchange $SCRIPT isotope-data.tsv plot-data/*
python $SCRIPT $3 >&2
