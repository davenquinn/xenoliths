from __future__ import division, print_function

import numpy as N
import fipy as F

from . import HalfSpaceSolver, FiniteSolver
from ..models import Section, Material
from ..units import u
from ..materials import continental_crust
from . import steady_state

def test_half_space():
    """ Test that the finite element model approaches parity
        with a simple half-space model.
    """
    # We define an oceanic mantle without
    # radiogenic heat generation
    oceanic_mantle = Material(
        conductivity = u(3.35,"W/m"),
        specific_heat = u(1171,"J/kg"),
        density = u(3300,"kg/m**3"))

    t = u(50,"Myr")

    layer = oceanic_mantle.to_layer(u(200,"km"))

    c = (u(25,"degC"),u(1500,"degC"))
    half_space = HalfSpaceSolver(layer, T_surface=c[0], T_max=c[1])

    section = Section([layer], uniform_temperature=c[1])
    finite = FiniteSolver(section, constraints=c)
    sol = finite(t, steps=50)
    hsol = half_space(t)

    f,h = tuple(i.profile for i in (sol, hsol))

    print("Maximum error: ",abs(f-h).max())
    assert N.allclose(f, h, atol=10)

def test_steady_state():
    """
    Test that we can create a steady-state model using
    FiPy that is similar to that given by our 'naive' solver
    """
    continental_crust.heat_generation = u(1,'mW/m^3')
    _ = continental_crust.to_layer(u(3000,'m'))
    section = Section([_])

    heatflow = u(100,'mW/m^2')
    surface_temperature = u(0,'degC')

    m = continental_crust
    q = heatflow
    k = m.conductivity
    a = m.heat_generation
    Cp = m.specific_heat
    rho = m.density

    def simple_heat_flow(x):
        # Density and heat capacity matter don't matter in steady-state
        T0 = surface_temperature
        return T0.to('K') + q*x/k + a/(2*k)*x**2

    p = simple_heat_flow(section.cell_centers)
    test_profile = p.into('degC')

    res = steady_state(section,heatflow, surface_temperature)
    profile = res.profile.into('degC')

    assert N.allclose(test_profile,profile)

    solver = FiniteSolver(_)
    solver.constrain(surface_temperature, None)
    solver.constrain(heatflow, None)

    # Concavity
    con = -a/k

    res2 = solver.steady_state()
    # Make sure it's nonlinear and has constant 2nd derivative
    arr = solver.var.faceGrad.divergence.value
    assert N.allclose(sum(arr-arr[0]),0)
    assert N.allclose(arr.mean(), con.into('K/m^2'))

    # Test simple finite element model
    mesh = F.Grid1D(
        nx=section.n_cells,
        dx=section.cell_sizes[0].into('m'))
    T = F.CellVariable(
        name="Temperature",
        mesh=mesh)
    T.constrain(surface_temperature.into("K"), mesh.facesLeft)
    A = F.FaceVariable(mesh=mesh, value=m.diffusivity.into("m**2/s"))
    rad_heat = F.CellVariable(mesh=mesh, value=(a/Cp/rho).into("K/s"))

    D = F.DiffusionTerm(coeff=A) + rad_heat
    D.solve(var=T)
    val = T.faceGrad.divergence.value
    arr = T.value-273.15
    assert N.allclose(val.mean(), con.into('K/m^2'))
    assert N.allclose(test_profile, arr)

    P = res2.profile.into('degC')
    assert N.allclose(test_profile,P)

