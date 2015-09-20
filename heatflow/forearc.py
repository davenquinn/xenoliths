from geotherm.units import u
from geotherm.models.geometry import Section
from geotherm.solvers import RoydenSolver
from geotherm.materials import oceanic_mantle, continental_crust

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
