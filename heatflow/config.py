from geotherm.units import u
from geotherm.materials import oceanic_mantle, continental_crust

surface_temperature = u(0,'degC')
# temperature of the base of the lithosphere
# used in the Royden model finite solving
asthenosphere_temperature = u(1450,"degC")

# Distance backarc of subduction zone for our
# final sections (influences Royden model evolution
# and duration of subduction).
underplating_distance = u(100,'km')

# Set conductivity to value from GDH model
oceanic_mantle.conductivity = u(3.138,"W/m/K")

# Depths
interface_depth = u(30,'km')
total_depth = u(500,'km')

# K-Ar age for Crystal Knob xenoliths
present = u(1.65,"Myr")

# Constraints for finite solver
solver_constraints = (
    surface_temperature,
    asthenosphere_temperature)
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

# Subduction velocity is just set at a reasonable value.
# Should make this a function of time based on plate circuit.
convergence_velocity = u(100,"mm/yr")
