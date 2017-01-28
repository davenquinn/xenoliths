from __future__ import division
from pandas import DataFrame
from figurator import tex_renderer, write_file
from uncertainties import ufloat
from calculations import T_CHUR, corrected_nd_ratio
from sys import argv

def build_data():
    data = DataFrame.from_csv("isotope-data.tsv",sep='\t')
    for id,row in data.iterrows():
        d = row.to_dict()
        d['id'] = id

        T = 1.65*1e6*365*24*3600
        d['143Nd/144Nd(T)'] = corrected_nd_ratio(row,T)

        d["T_CHUR"] = round(T_CHUR(row, T),2)

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
