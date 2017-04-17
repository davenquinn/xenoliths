from __future__ import division
from dofile import redo_ifchange
from pandas import DataFrame
from figurator import tex_renderer, write_file
from uncertainties import ufloat
from calculations import T_CHUR, sample_nd_ratio, sample_sr_ratio
from sys import argv

table_data = "isotope-data.tsv"
redo_ifchange(table_data)

def build_data():
    data = DataFrame.from_csv(table_data,sep='\t')
    for id,row in data.iterrows():
        d = row.to_dict()
        d['id'] = id

        T = 1.65*1e6 # years
        d['143Nd/144Nd(T)'] = sample_nd_ratio(row,T)
        d['87Sr/86Sr(T)'] = sample_sr_ratio(row,T)
        d['deltaNd'] = (d['143Nd/144Nd(T)']-d['143Nd/144Nd(0)'])*1e6
        d['deltaSr'] = (d['87Sr/86Sr(T)']-d['87Sr/86Sr(0)'])*1e7

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
