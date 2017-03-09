
from pint import UnitRegistry
from pint.unit import DimensionalityError

unit = UnitRegistry()

unit.define('yr = 1 * year')

class Quantity(unit.Quantity):
    def into(self,u):
        a = self.to(u)
        return a.magnitude

def ensure_unit(q,default):
    """Applies the default unit if no unit is applied"""
    try:
        return q.to(default.units)
    except AttributeError:
        return q * default

def u(number, un):
    return Quantity(number, un)
