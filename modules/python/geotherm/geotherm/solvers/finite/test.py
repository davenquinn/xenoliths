import numpy as N
import fipy as F

from ...test import simple_profile
from .simple import SimpleFiniteSolver
from .advanced import AdvancedFiniteSolver as FiniteSolver
from ...models import Section, Material
from ...units import u
from ...materials import continental_crust


class TestMeshes(object):
    def __init__(self):
        self.section = simple_profile()
        self.solver = FiniteSolver(self.section)

    def test_mesh_creation(self):
        mesh = self.solver.create_mesh()
        d = mesh.cellCenters - self.section.cell_centers.into("m")
        assert d.all() == 0

def test_radiogenic_heat():
    """
    Test that the finite element model
    properly accounts for added heat from radiogenic heating
    """
    def one_step(material):
        constraints = tuple(u(i,"degC")
                for i in (25,1500))
        lyr = material.to_layer(u(200,"km"))
        section = Section([lyr])\
            .linear_geotherm(*constraints)
        finite = FiniteSolver(section)
        return finite(u(1,"Myr"),steps=10).profile

    continental_crust.heat_generation = u(1,"uW/m**3")
    cr = one_step(continental_crust)

    continental_crust.heat_generation = u(0,"mW/m**3")
    cr2 = one_step(continental_crust)

    diff = (cr-cr2)
    # Test that radiative heat generation produces positive
    # results
    print(("Maximum difference: {0}".format(diff.max())))
    assert N.all(diff.magnitude >= 0)
    assert N.sum(diff.magnitude) > 0
