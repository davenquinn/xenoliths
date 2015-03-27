from .models.material import Material
from .units import u

oceanic_mantle = Material(
    conductivity = u(3.35,"W/m/K"),
    specific_heat = u(1171,"J/kg/K"),
    density = u(3300,"kg/m**3"),
    heat_generation = u(0.006,"uW/m**3"))

continental_crust = Material(
    conductivity = u(2.5,"W/m/K"),
    specific_heat = u(1000,"J/kg/K"),
    density = u(2800,"kg/m**3"),
    heat_generation = u(1,"uW/m**3"))

oceanic_crust = Material(
    conductivity = u(2.9,"W/m/K"),
    specific_heat = u(1050,"J/kg/K"),
    density = u(3100,"kg/m**3"),
    heat_generation = u(0.5,"uW/m**3"))
