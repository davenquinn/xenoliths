from .units import u
from .models.material import Material
from .models.geometry import Layer, Section, stack_sections
from .materials import continental_crust

def simple_profile():
    material = Material()
    a = Section([
        Layer(material, u(10,"km")),
        ], uniform_temperature=u(200,"degC"))

    b = Section([
        Layer(material, u(10,"km")),
        ], uniform_temperature=u(800,"degC"))
    return stack_sections(a,b)

def realistic_profile():
    oceanic_mantle = Material(
        conductivity = u(3.35,"W/m/K"),
        specific_heat = u(1171,"J/K/kg"),
        density = u(3300,"kg/m**3")
    )
    continental_crust = Material(
        conductivity = u(2.5,"W/m/K"),
        specific_heat = u(1000,"J/K/kg"),
        density = u(2800,"kg/m**3")
    )

    # Initialize oceanic crust (analytical)
    oceanic = HalfSpaceSolver(Layer(oceanic_crust, u(100,"km")))
    evolved_oceanic = oceanic.solution(u(30,"Myr"))

    # Will put royden solver here.

    # Initialize continental crust (analytical)
    evolved_forearc = Section([Layer(continental_crust, u(30,"km"))], uniform_temperature=u(200,"degC"))

    # Stack the two of them
    return stack_sections(
        evolved_forearc.get_slice(u(0,"km"), u(30,"km")),
        evolved_oceanic.get_slice(u(0,"km"),u(70,"km"))
        )

def test_radiogenic_units():
    """
    Tests unit conversion for the creation of a radiogenic
    heating term.
    """
    cr = continental_crust
    term = cr.heat_generation/cr.specific_heat/cr.density
    assert term.dimensionality == u(1,"K/s").dimensionality
