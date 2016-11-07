from __future__ import division
import numpy as N
from geotherm.units import u
from heatflow.config import (
    continental_crust,
    oceanic_mantle, interface_depth)
from .pressure import geobaric_gradient, simple_geobaric_gradient

def test_geobaric_gradient():
    assert geobaric_gradient(0) == simple_geobaric_gradient(0) == 0

    assert N.allclose(
        geobaric_gradient(1),
        simple_geobaric_gradient(1),
        rtol=0.1)
