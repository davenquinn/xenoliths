from pandas import DataFrame
from paper.text import tex_renderer, write_file

from IPython import embed

data = DataFrame.from_csv("isotope-data.tsv",sep='\t')

write_file("build/isotopes-table.tex", data.to_latex())
