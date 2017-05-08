# Supplementary information for modeling setup {#sec:model_supplement}

## Model setups

Standardized model parameters used in the models are justified
in the text below. Standard values for thermal conductivity from
@Fowler2005 yield good results.
Increasing the thermal conductivity of the model domain
substantially depresses the modeled geotherms (lowering predicted
temperatures at a given depth), but does not affect the
relative temperatures predicted by the geotherms.
Radiogenic heat flow for the continental marginal crust
is estimated conservatively, and changes result in only minor changes to modeled geotherms
across the board.

### Slab window crustal replacement

In series **A**, we model shallow slab-window upwelling.
The emplacement of slab-window
asthenosphere directly under the coastal central California crust
entails the truncation of a low-temperature forearc geotherm at the base of the crust
and the substitution of an asthenospheric adiabat below
this level.  The model begins at 24 Ma, corresponding to the time of
opening of the Mendocino slab window under southern California
[@Wilson2005].  The geotherm begins as a steady-state profile to 600 ºC
at 30 km, truncated by a mantle adiabat.  The mantle is held at
asthenospheric conditions for a set period which is varied between model
runs (from 0 to 6 Myr) to simulate a period of active convection, after
which it relaxes conductively to the conclusion of the model.

### Subduction and underplating

Thermal conditions
during subduction are tracked using the @Royden1993a steady-state
forearc model. The samples then relax to the present. After subduction
and underplating, the cooled oceanic lithosphere re-equilibrates with an
overlying 30 km of forearc crust until the present, or for our xenolith
samples until the time of ca. 1.7 Ma entrainment and eruption. 

Progressive subduction of the downgoing slab beneath the forearc wedge
is modeled as stepwise advection beneath a linearly thickening forearc
wedge conforming to the @Royden1993a thermal model using the parameters
outlined above.  For all cases, the final depth of the underplated
subduction interface is taken to be 30 km, and the distance landward of
the subduction zone is taken to be 100 km.  No effort is made to
differentiate 'flat-slab' and baseline subduction geometries. Though
increasing the slab dip angle will result in a cooler subduction
interface at a given depth, the overall effect on the evolution of the
thermal scenarios appears to be minimal.

### Oceanic geotherm

For the Neogene stalled Monterey plate and Late Cretaceous Farallon
mantle nappe scenarios, the Global Depth and Heat (GDH) model
[@Stein1992] is used to trace the thermal evolution of the oceanic
lithosphere from its emplacement at the spreading ridge until
subduction.  This model is a Taylor-polynomial fit of cooling parameters
to global heat-flow and depth datasets. This fit yields higher geotherms
than half-space cooling models that are directly based on @eq:heat_flow
(e.g., @Fowler2005), and tends to produce higher geotherms for old
oceanic lithosphere.

With the GDH model in conjunction with the @Royden1993a subduction model,
we predict low temperatures (~235-245 ºC) at the subduction
interface for the oldest stalled slabs modeled. For the Monterey Plate
scenario (with young oceanic
crust) the temperature at the subduction interface is predicted to be
980 ºC.

All oceanic-cooling models, including GDH and half-space cooling
models, significantly overestimate heat flux from young oceanic plates,
a fact that is likely attributable to vigorous hydrothermal circulation
in young submarine lithosphere [@Stein1992;@Stein1995].  This may result
in overestimates of geothermal gradients for the scenarios with the
youngest subducted oceanic crust, such as the Monterey Plate scenario at
the left of @fig:model_tracers.

### Supra-subduction geotherm

The geotherm of the forearc wedge during subduction is calculated using
the @Royden1993a analytical solution for the steady-state thermal
structure of continuously-subducting systems.  Shear heating on the
subduction thrust is ignored, as recent studies suggest that it is not
an important factor [@Kidder2013]. Forearc rock uplift and erosion, as
well as accretion and erosion on the subduction megathrust are ignored.
In reality, megathrust accretion rates of 0.2-3.6 km/Myr are favored by
@Kidder2013 based on the Pelona schist, and some rock uplift is evident
for the Coast Ranges.

The coastal California accretionary crust is represented homogenously as
a material with a thermal conductivity of 2.71 W/m/K, specific heat
capacity of 1000 J/kg/K, density of 2800 kg/m^3 and a radiogenic heat
flux of 2 uW/m^3, values that are close to average for the continental
crust [@Fowler2005] and those used by @Kidder2013 to model the thermal
conditions along the Late Cretaceous shallow subduction megathrust
segment.  A radiogenic heat production in the crust of 2 uW/m^3 is
actually a relatively conservative estimate given the fluxes shown for
Sierra Nevada batholithic material by @Brady2006, and the fact that much
of the Franciscan material within the subduction channel is pelitic
sediment rich in radiogenic elements [@Vila2010]. Still, lower
radiogenic heat production in the crust yields only a slight decrease in
modeled geotherms across the board, not impacting conclusions.

## Factors not incorporated into the model

Several simplifications are made to create an internally consistent model framework.
Subducted oceanic
crust is not considered to have distinct thermal properties from the
oceanic mantle.
Additionally, though
there are no reliable estimates of the mantle heat flux that cover the
model domain, the model is run to great depth to avoid any influence of
this uncertainty on the surface geotherm.

### Subduction zone rollback

The confounding factor of an active subduction zone just outboard of the
scenarios for the older models is also not included within the model.
When the trench interface jumps with the emplacement of an oceanic
mantle nappe beneath the forearc, the new subduction interface will cool
the detached nappe from below. This is not modeled because it would
substantially increase model complexity (requiring a fully iterative
approach to the forearc geotherm), and at this distance (~100 km)
inboard of the final trench interface, there is limited scope for
further episodic rollback after emplacement of the nappe(s) of presumed
xenolith source [e.g. Figure @fig:neogene_sections|c].  Further,
although an active subduction interface at depth will cool the mantle
lithosphere from below, the subduction of progressively younger crust
until cessation at ~27 Ma will yield gradually increasing heat on the
subduction interface [@Royden1993a]. The models for scenarios **B** and **C**
[@fig:model_comparisons|b and c]
are already near the coolest
permitted by our xenolith constraints.  As these geotherms are already
quite cold, introducing this added complexity will not significantly
change the model results.  However, late-Creteaceous underplating and other stalled-slab scenarios can
be treated as maximum temperatures because of the influence of the
subducting slab.

### Change in convergence rate of rotating microplates

Potential Monterey
Plate mantle lithosphere beneath Crystal Knob would have been emplaced
under the ridge at 27 Ma (corresponding to the chron 7 magnetic anomaly)
and subducted shortly thereafter [@Atwater1998; @Wilson2005]. 
Due to slower margin-normal convergence during microplate fragmentation and
rotation [@Wilson2005], the parcel would take ~3 Myr to reach its final
stalled position (~100 km behind the trench) as shown in Figure
@fig:neogene_sections|b. This is responsible for the kink in the "Age of initial oceanic lithosphere" curve in @fig:model_tracers|b. For model simplicity, we do not
incorporate this disequilibrium shift into the starting parameters of the @Royden1993a subduction model.

### Erosion of the forearc

Surface erosion after underplating is taken to be zero. Any erosion will
result in higher apparent heat flow values and increased geotherm
convexity, as heat is advected from the
top of the model domain by material removal.
Geologic constraints suggest that
the majority of erosion to the mid-crustal levels now
at the surface in Salinia is likely to have occurred in a major pulse of
unroofing coincident with flat-slab underplating and rollback
[@Saleeby2003; @Chapman2012], and is thus likely to disproportionately
affect the older models. However, the 30 km of crust shown in the study
area is based on modern estimates of the Moho depth, so recent erosion
is unlikely to have biased the whole-lithosphere geotherm significantly.
Still, the lack of erosion in the model framework will likely bias the
results towards predicting lower geothermal gradient overall, as upward
advection of material by erosion increases the geothermal gradient
[@Mancktelow1997;@England1990].

