SCRIPT=generate-table.py

redo-ifchange $SCRIPT templates/isotopes.tex isotope-data.tsv
python $SCRIPT $3 >&2
