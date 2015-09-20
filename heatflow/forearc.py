from geotherm.units import u
from geotherm.models.geometry import Section
from geotherm.solvers import RoydenSolver
from geotherm.materials import oceanic_mantle, continental_crust
from scipy.optimize import minimize_scalar

def optimized_forearc(target,distance,depth, **kwargs):
    """
    Returns Royden model forearc geotherm
    that is optimized to return a certain
    temperature at the subduction interface.
    """
    opt = kwargs.pop('vary','Au')

    solver = forearc_solver(**kwargs)

    target = target.into("degC")
    d = distance.into("m")
    Z = depth.into("m")

    def f(v):
        solver.args[opt]=v
        t = solver.royden(d, Z, Z)
        a = abs(target-t)
        return a

    o = minimize_scalar(f,
            bounds=(0,1e9),
            method='bounded')
    solver.args[opt] = o.x
    return solver

def forearc_solver(**kwargs):
    defaults = dict()
    defaults.update(kwargs)

    royden = RoydenSolver(**defaults)
    return royden

def forearc_section(**kwargs):
    # Thickness of the forearc wedge
    thickness = kwargs.pop("thickness", u(30, "km"))

    # Distance from the subduction interface
    distance = kwargs.pop("distance",u(30,"km"))

    # In case we have a royden solver we want to use
    solver = kwargs.pop("solver",None)
    if not solver:
        solver = forearc_solver(**kwargs)

    forearc = Section([continental_crust.to_layer(thickness)])
    temperatures = solver(distance.into("m"),
            forearc.cell_centers.into("m"),
            thickness.into("m"))

    forearc.profile = u(temperatures, "degC")

    return forearc
