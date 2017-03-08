#!/usr/bin/env python
from __future__ import division

from xenoliths.thermometry.pressure import geobaric_gradient, simple_geobaric_gradient

## Get the average geobaric gradient at 3 GPa
depth = geobaric_gradient(3)
gg = lambda i: i/geobaric_gradient(i)
print("Average geobaric gradient: {:.3f} GPa/km (to 1 GPa)".format(gg(1)))
print("                           {:.3f} GPa/km (at 3 GPa)".format(gg(3)))
print("Simple geobaric gradient:  {:.3f} GPa/km".format(1/simple_geobaric_gradient(1)))
