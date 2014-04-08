from .models.material import Material
from .units import u

oceanic_mantle = Material(
    conductivity = u(3.35,"W/m"),
    specific_heat = u(1171,"J/kg"),
    density = u(3300,"kg/m**3"))

continental_crust = Material(
    conductivity = u(2.5,"W/m"),
    specific_heat = u(1000,"J/kg"),
    density = u(2800,"kg/m**3"))
