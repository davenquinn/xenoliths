from __future__ import division
from pandas import DataFrame
from sys import argv
import numpy as N
from matplotlib import pyplot as P

data = DataFrame.from_csv("isotope-data.tsv",sep='\t')

x = data["87Sr/86Sr(0)"]
y = data['Epsilon Nd']

fig = P.figure()
ax = fig.add_subplot(111)
ax.plot(x,y, "ko")

ax.set_xlabel(r'$^{87}$Sr/$^{86}$Sr')
ax.set_ylabel(r"$\epsilon_{Nd}$")
ax.set_ylim([-5,12])
ax.set_xlim([0.7015,0.708])
ax.annotate("Crystal Knob",
        xy=(x.mean(),y.mean()), xycoords="data", textcoords="offset points", xytext=(15,-4))

ax.axhline(y=0, color="#999999", linestyle="dotted")
ax.axvline(x=.7045, color="#999999", linestyle="dotted")

# Bulk earth from DePaolo and Wasserburg, 1976
ax.annotate("Bulk Earth", xy=(.7045,0), xycoords="data", textcoords="offset points", xytext=(5,5))

fig.savefig(argv[1], bbox_inches="tight")

