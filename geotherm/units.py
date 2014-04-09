from __future__ import division
from pint import UnitRegistry
from pint.unit import DimensionalityError

unit = UnitRegistry()

unit.define('yr = 1 * year')

class Quantity(unit.Quantity):
    def __init__(self,*args):
        super(unit.Quantity,self).__init__(*args)

    def into(self,u):
        a = self.to(u)
        return a.magnitude

def ensure_unit(q,default):
    """Applies the default unit if no unit is applied"""
    try:
        return q.to(default)
    except AttributeError:
        return q * default

def u(number, un):
    return Quantity(number, un)
