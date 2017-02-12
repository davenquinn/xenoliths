#!/bin/env/python
# -*- coding:utf-8 -*-
from sys import argv
from pandas import read_excel, isnull
from uncertainties import ufloat
from IPython import embed
from figurator import tex_renderer

def make_uncertain(df, index, uncertain_index=None):
    """
    Combine column of standard values with column
    representing standard deviations
    """
    if uncertain_index is None:
        uncertain_index = index+1
    ix = df.columns[[index,uncertain_index]]
    val = df[ix].apply(lambda i: ufloat(i[0],i[1]), axis=1)
    val.name = df.ix[:,index].name
    df.ix[:,index] = val
    df.drop(df.columns[uncertain_index],axis=1,inplace=True)

def ratio(top, btm):
    serie = df[top]/df[btm]
    serie.name = "{}/{}".format(top,bottom)
    return serie

df = read_excel(argv[1], header=1, index_col=0)
#df.drop(df.columns[range(10)], axis=1, inplace=True)
# I don't know what this stupid column means
df.drop([u"±1s"],axis=1, inplace=True)
df.dropna(inplace=True)

# Condense all columns with uncertainties into
# single ufloat columns
cols = list(range(5))+[7,8,10]
for i in cols:
    make_uncertain(df, i)

btm = '39Ar'
for i in [40,38,37,36]:
    st = str(i)+"Ar"
    series = df[st]/df[btm]
    lbl = st+"/"+btm
    df.insert(0,lbl,series)
    df.drop(st,axis=1,inplace=True)
df.drop(btm,axis=1,inplace=True)

text = (tex_renderer
    .get_template('lava-age.tex')
    .render(data=df.iterrows()))

embed()

with open(argv[2],'w') as f:
    f.write(text)


