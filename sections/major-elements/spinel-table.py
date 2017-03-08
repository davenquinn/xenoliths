import numpy as N
from sys import argv
from query import spinel_data
from collections import defaultdict
from spinel_calc import correct_spinel
from figurator import tex_renderer, write_file
from xenoliths import app
from uncertainties import ufloat

def uncertain_array(v):
    arr = N.array(v)
    return ufloat(arr.mean(),arr.std())

with app.app_context():
    data = spinel_data()
    corrected = [correct_spinel(s,uncertainties=False) for s in data]

    sample_data = defaultdict(list)

    for d in data:
        sample_data[d.sample.id].append(dict(
            data=d,
            corrected = correct_spinel(d,uncertainties=False)))

    rows = []
    for k,row in sample_data.items():
        raw = [i.pop('data') for i in row]
        corr = [i.pop('corrected') for i in row]

        r = dict()
        r['sample_id'] = k
        r['Fe'] = uncertain_array([i['Fe'] for i in corr])
        r['Fe(III)'] = uncertain_array([i['Fe(III)'] for i in corr])
        r['fe_ratio'] = r['Fe(III)']/(r['Fe']+r['Fe(III)'])
        r['mg_number_raw'] = uncertain_array([c.mg_number for c in raw])
        r['mg_number_corr'] = uncertain_array([c['Mg']/(c['Mg']+c['Fe'])*100
                                      for c in corr])
        r['n'] = len(raw)

        rows.append(r)

text = (tex_renderer
    .get_template("corrected-spinels.tex")
    .render(data=sorted(rows,key=lambda d: int(d['sample_id'][-1]))))
write_file(argv[1],text)
