#!/usr/bin/env python
from __future__ import division
import IPython
import fipy as F
import numpy as N
from scipy.special import erf


ny = 50
dy = 1.
mesh = F.Grid1D(nx=ny, dx=dy)

phi = F.CellVariable(name="solution variable", 
                   mesh=mesh,
                   value=0.)

D = 1.

valueTop = 1
valueBottom = 0

phi.constrain(valueBottom, mesh.facesRight)
phi.constrain(valueTop, mesh.facesLeft)

eqX = F.TransientTerm() == F.ExplicitDiffusionTerm(coeff=D)

# 0.9 * Largest stable timestep
timeStepDuration = 0.9 * dy**2 / (2 * D)
steps = 100

phiAnalytical = F.CellVariable(name="analytical value", mesh=mesh)

if __name__ == '__main__':
    viewer = F.Viewer(vars=(phi, phiAnalytical), datamin=0., datamax=1.)
    viewer.plot()

y = mesh.cellCenters[0]
t = timeStepDuration * steps

phiAnalytical.setValue(1 - erf(y / (2 * N.sqrt(D * t))))

for step in range(steps):
    eqX.solve(var=phi,
              dt=timeStepDuration)
    if __name__ == '__main__':
        viewer.plot()

IPython.embed()
