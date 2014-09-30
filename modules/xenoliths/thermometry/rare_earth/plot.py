# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as P
import periodictable as pt
import numpy as N
from .calc import ree_pyroxene, rare_earths
import statsmodels.api as sm
from uncertainties import ufloat

elements = sorted(pt.elements, key=lambda x: x.number)


def setup_figure():
    fig = P.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.set_ylabel("B")
    ax.set_xlabel(r"$ln(D)-A$")
    return fig, ax

def regress(X,Y):
    model = sm.RLM(Y,X, M=sm.robust.norms.TukeyBiweight())
    res = model.fit()
    kelvin = res.params[0]
    res.temperature = kelvin-273.15
    # Make sure that the regression goes through the origin
    assert N.allclose(res.fittedvalues/kelvin,X)
    return res

def temperature(results, uncertainty=True):
    T = results.params[0]-273.15
    if uncertainty:
        return ufloat(T, results.bse[0]) # B-hat standard error (std. error of estimator)
    else:
        return T

def plot_DREE(sample):
    X,Y = ree_pyroxene(sample, 1.5)
    res = regress(X,Y)
    T = temperature(res)

    fig, ax = setup_figure()
    fig.suptitle(u"{id}: {n:.0f}±{s:.0f} °C".format(
        id=sample.id,
        n=T.n,
        s=T.s))
    ax.plot(X,Y, "o")
    ax.plot(X,res.fittedvalues,"-")

    for x,y,t in zip(X,Y,rare_earths):
        ax.annotate(t, (x,y), xytext=(5,5), textcoords="offset points")
    return fig

def ree_temperature(sample, **kwargs):
    uncertain = kwargs.pop("uncertainties", True)
    X,Y = ree_pyroxene(sample, **kwargs)
    return temperature(regress(X,Y), uncertain)
