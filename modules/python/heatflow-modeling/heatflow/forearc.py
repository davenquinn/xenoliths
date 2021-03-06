from geotherm.units import u
from geotherm.models.geometry import Section
from geotherm.solvers import RoydenSolver
from scipy.optimize import minimize, minimize_scalar
from click import echo

from .config import (
    asthenosphere_temperature,
    forearc_base_temperature,
    interface_depth,
    oceanic_mantle, continental_crust)

class ScalableRoydenSolver(RoydenSolver):
    def royden(self, *args):
        s = self.args.get('scalar',1)
        val = RoydenSolver.royden(self,*args)
        return val*s

def optimized_forearc(target,distance,depth, **kwargs):
    """
    Returns Royden model forearc geotherm
    that is optimized to return a certain
    temperature at the subduction interface.
    """
    opt = kwargs.pop('vary','qfric')

    solver = forearc_solver(**kwargs)

    target = target.into("degC")
    d = distance.into("m")
    Z = depth.into("m")
    sz = interface_depth.into("m")
    echo("Optimizing {} to target".format(opt))

    def f(v):
        solver.args[opt]=v
        t = solver.royden(d, Z, sz)[0]
        a = (target-t)**2
        return a

    o = minimize(f,0)#,
            # bounds=(0,1e9),
            # method='bounded')
    solver.args[opt] = o.x[0]

    # Determine max temperature in forearc
    def f(depth):
        return -solver.royden(d,depth,sz)
    o = minimize_scalar(f,
            bounds=(0,Z),
            method='bounded')
    echo("Maximum temperature above interface:")
    echo(solver.royden(d,o.x,Z))
    echo(f"at depth {o.x} meters")

    echo("Optimal value:")
    echo("  {} = {}".format(opt,solver.args[opt]))

    return solver

def forearc_solver(**kwargs):
    m = oceanic_mantle
    c = continental_crust

    defaults = dict(
        Tm = forearc_base_temperature.into("degC"),
        Al=m.heat_generation.into('W/m**3'),
        Au=c.heat_generation.into('W/m**3'),
        Kl=m.conductivity.into('W/m/K'),
        Ku=c.conductivity.into('W/m/K'),
        zr=150e3,
        #a=1e-15, # No sub. accretion or erosion
        #e=1.e-9,
        qfric=0,
        alpha=m.diffusivity.into('m**2/s'))
    defaults.update(kwargs)

    royden = ScalableRoydenSolver(**defaults)
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
