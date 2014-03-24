from __future__ import division
from pint import UnitRegistry

registry = UnitRegistry()
quantity = registry.Quantity

def ensure_unit(q,default):
    """Applies the default unit if no unit is applied"""
    try:
        return q.to(default)
    except AttributeError:
        return q * default
