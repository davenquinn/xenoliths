# Supplementary file: modeling setup {#sec:model_supplement}

## Model setups

Standardized parameters used in modeling are justified
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

## Model sensitivity and bias {#sec:model_bias}

Generally, changes in model parameters such as radiogenic heat flux,
thermal conductivity, and heat capacity do not impact the relative
results for modeled scenarios, due to the consistent lithologic
structure of the model domains.

Due to widely varying timescale of equilibration for modeled scenarios
in groups **B** and **C**, the model is sensitive to assumptions
about steady-state cooling of the oceanic mantle lithosphere.
The choice of the "GDH" model to track the evolution of
the suboceanic thermal structure is an important control on the scale of
temperature variation in @fig:model_tracers|b.
Though GDH is well-calibrated, oceanic cooling models tend to overestimate the heat flow from
young oceanic plates [@Stein1995]. Thus, the modeled geothermal gradients for the
younger stalled slab model runs may be too high.

Another potential confounding factor affecting the older scenarios
of **B** and **C** is the thermal effects of continued subduction
beneath the underplated mantle nappes. After rollback and underplating of the modeled section of
oceanic mantle lithosphere, a downgoing slab at depth could, depending
on its age, cool the forearc lithosphere from below.
However, this effect is considered minimal and
diminishes over time due to the progressive subduction of younger, hotter oceanic
lithosphere.
Reconstruction of the Pacific--Farallon spreading ridge history show
that, between ca. 70 and 30 Ma, oceanic lithosphere entering the
southwest Cordilleran subduction zone got younger at a rate of ~1
Myr/Ma [@Atwater1998; @Liu2010; @Seton2012] corresponding to the
approach of the ridge to the subduction zone. This factor coupled with
slab window emplacement starting at ca. 24 Ma leads to the
interpretation that cooling from below by continued subduction
was of second-order significance.

Surface erosion is not modeled, but may bias the results. Any erosion will
yield higher apparent heat flows and increased geotherm
convexity, as heat is advected from the
top of the model domain by material removal [@Mancktelow1997;@England1990].
Geologic constraints suggest that 15-20 km of exhumation
is likely to have occurred in a major pulse of
unroofing coincident with flat-slab underplating and rollback in the
Cretaceous [@Saleeby2003; @Chapman2012], and is thus likely to disproportionately
affect the older models. The lack of erosion in the model framework
biases towards predicting lower geothermal gradient overall.
For the slab window and underplated Monterey plate scenarios (model
groups **A** and **B**) this effect would push the final geotherm to or
beyond the limit of xenolith thermobarometry [@fig:model_results|a and b].
In the underplated mantle nappe scenario (model **C**) this effect would
push the final modeled geotherm towards the centroid of the xenolith
thermobarometric array [@fig:model_results|c and @fig:model_comparison]

The uncertainties inherent in this model bias the results
towards predicting lower-temperature,
less-convex geotherms over the model domain.
These potential biases affect comparisons comparisons with measured values of
heat flux and xenolith thermobarometry, which are not subject to these
biases [@fig:model_comparison]. Thus, geotherms predicted by this model might be underestimates
for potential mantle temperature at a given depth, especially for the
older tectonic scenarios modeled.

## Factors not incorporated in the model

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
result in higher apparent heat flow values and increased geotherm convexity,
as heat is advected from the top of the model domain by material removal.
Geologic constraints suggest that the majority of erosion to the mid-crustal
levels now at the surface in Salinia is likely to have occurred in a major
pulse of unroofing coincident with flat-slab underplating and rollback
[@Saleeby2003; @Chapman2012], and is thus likely to disproportionately affect
the older models. The 30 km of crust shown in the study area is based on
modern estimates of the Moho depth, so recent erosion is unlikely to have
biased the whole-lithosphere geotherm significantly. Still, the lack of
erosion in the model framework will likely bias the results towards predicting
a lower geothermal gradient overall, and lower temperatures in the mantle
lithosphere, as upward advection of material by erosion increases the
geothermal gradient [@Mancktelow1997;@England1990]. Thus, these values need to
be biased to higher temperatures to accurately capture the relationship
between xenolith constraints on the actual temperature and temperatures
derived from this modeling.

