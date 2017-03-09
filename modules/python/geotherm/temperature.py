#!/usr/bin/env python


from geotherm.units import u
from geotherm.plot import ComparisonPlotter, Plotter
from geotherm.models.geometry import Section
from geotherm.materials import oceanic_mantle
from geotherm.solvers import HalfSpaceSolver, AdvancedFiniteSolver

layer = oceanic_mantle.to_layer(u(100,"km"))
section = Section([layer], uniform_temperature=u(1500,"degC"))
finite = AdvancedFiniteSolver(section)
half_space = HalfSpaceSolver(section)

plotter = ComparisonPlotter(
    half_space.profile,
    title="Half-space test",
    range=(0,2000))
#plotter = Plotter(range=(0,2000))
finite.solution(u(3,"Myr"), plotter=plotter)