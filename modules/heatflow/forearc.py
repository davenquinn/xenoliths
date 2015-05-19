from geotherm.units import u
from geotherm.models.geometry import Section
from geotherm.solvers import RoydenSolver
from geotherm.materials import oceanic_mantle, continental_crust

def forearc_solver(**kwargs):
    defaults = dict(
            Al=oceanic_mantle.heat_generation.into("W/m**3"),
            Au=continental_crust.heat_generation.into("W/m**3"),
            Kl=oceanic_mantle.conductivity.into("W/m/K"),
            Ku=continental_crust.conductivity.into("W/m/K"),
            # No subduction accretion or erosion
            a=u(0,"m/Myr").into("m/s"),
            e=u(0,"m/Myr").into("m/s"),
            zr=120e3)

    defaults.update(kwargs)

    royden = RoydenSolver(**defaults)
        # temperature at the base of the lithosphere (degrees C)
        #Tm=1300,
        ##   thickness of the lithosphere
        #l=90e3,
        ##   radiogenic heat production  (W/m3)
        #Al=1e-9, #lower plate
        #Au=1e-6, #upper plate
        ##   heat conductivity in each plate  (W/m.K)
        #Kl=2.5, #lower plate
        #Ku=2.5, #upper plate
        ##   depth to the base of the radiogenic layer in foreland (m)
        #zr=30e3,
        ##   rate of accretion (m/s)
        #a=0,
        ##   rate of erosion (m/s)
        #e=0,
        ##   rate of under thrusting (m/s)
        #v=20.*1e-3/(365*24*3600),
        ##   thermal diffusivity  (m2/s)
        #alpha=1e-6,
        ##   heat flow due to friction on fault (tau*v) (W/m2)
        #qfric=15.*1e-3)
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
