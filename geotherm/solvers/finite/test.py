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

def test_simple_case():
    material = Material()
    layer = Layer(material, u(100,"km"), grid_spacing=u(100,"m"))
    simple = SimpleFiniteSolver(layer)
    advanced = AdvancedFiniteSolver(layer)
    time = u(100,"kyr")
    s = simple.solve()

    for solS, solA in zip(s,a):
        pass
