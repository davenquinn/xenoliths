from __future__ import division
from pandas import DataFrame
from paper.text import tex_renderer, write_file
from uncertainties import ufloat
from sys import argv

def build_data():
    data = DataFrame.from_csv("isotope-data.tsv",sep='\t')
    for row in data.iterrows():
        d = row[1].to_dict()
        d['id'] = row[0]
        for i,s in [('143Nd/144Nd(0)','std err%'),
                  ('87Sr/86Sr(0)','std err%.1')]:
            s = d.pop(s)
            d[i] = ufloat(d[i],s/100*d[i])
        d.pop('Sm/Nd')
        d.pop('Rb/Sr')
        yield d

text = (tex_renderer
    .get_template("isotopes.tex")
    .render(samples=build_data()))

write_file(argv[1], text)
