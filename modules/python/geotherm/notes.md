# Current progress

- Two-layer model (oceanic mantle, continental crust)
- Bottom constraint (1500ºC) looks pretty weird. Obviously messing things up
- No radiogenic heat production
- No oceanic crust
- Continental forearc geotherm is not well-defined. Should probably use Royden's model
- Not sure how accurate implicit solution is...relatively few time-steps used


## Need to implement

- Radiogenic heat production in crust
- Constant-flux constraint for bottom of section (instead of absolute temperature)
- Adiabatic temperature gradient for underplated mantle
- Crank-Nicholson scheme for more accurate solutions

## Outstanding questions

1. Should I use a half-space model (or GDH) to model initial purely oceanic sections? These only make allowance for one set of physical properties (i.e. oceanic mantle) and neglect the oceanic crust entirely. For starters, I am going to neglect oceanic crust, because that seems to provide a way forward using only the half-space model to define the first part of the evolution. A possible alternative is to use finite difference with oceanic crust and mantle defined separately, and initialized from an adiabatic temperature gradient.
2. How should I treat forearc geotherms (on hanging wall of subduction underplating)? Should I use the Royden et al. model, as suggested by Jean-Philippe? Right now I am just initializing them at a constant temperature.
3. I know I should use constant-temperature constraint at the surface, but should I use this or a constant-flux constraint at the bottom of the section (mantle)? I think the best would be a constant-flux constraint...need to figure out what this would be.
