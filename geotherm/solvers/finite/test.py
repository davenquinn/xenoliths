from ...test import simple_profile
from .simple import SimpleFiniteSolver
from .advanced import AdvancedFiniteSolver
import fipy as F
import IPython

class TestMeshes(object):
    def __init__(self):
        self.section = simple_profile()
        self.solver = AdvancedFiniteSolver(self.section)

    def test_mesh_creation(self):
        mesh = self.solver.create_mesh()
        d = mesh.cellCenters - self.section.cell_centers.into("m")
        assert d.all() == 0

