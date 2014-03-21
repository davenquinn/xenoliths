#!/usr/bin/env python
from __future__ import division
import IPython
import fipy as F
import numpy as N
from scipy.special import erf

from half_space import HalfSpace, MaterialModel

Ma = lambda s: s/3.15569e11
seconds = lambda Ma: 3.15569e11*Ma

material = MaterialModel()
half = HalfSpace(material)

depth = 1e5 #m
dy = 10
ny = int(depth/dy)
mesh = F.Grid1D(nx=ny, dx=dy)

val = [half.T_max]*ny

phi = F.CellVariable(name="solution variable", mesh=mesh, value=val)
phi.constrain(0, mesh.facesRight)
phi.constrain(half.T_max, mesh.facesLeft)

# 0.9 * Largest stable timestep for explicit differentiation
time_step = 0.9 * dy**2 / (2 * material.diffusivity)
print time_step
# Implicit diffusion: sacrifice accuracy for speed
eqX = F.TransientTerm() == F.DiffusionTerm(coeff=material.diffusivity)
time_step = seconds(0.1)
print "Time step: {0}".format(Ma(time_step))

steps = 400

print "Total time: {0}".format(Ma(time_step*steps))



if __name__ == '__main__':
    viewer = F.Matplotlib1DViewer(vars=(phi), datamin=0., datamax=2000., legend="lower right")
    viewer.plot()

for step in range(steps):
    eqX.solve(var=phi,
              dt=time_step)
    if __name__ == '__main__':
        viewer.plot()
        print Ma(step*time_step)

IPython.embed()
