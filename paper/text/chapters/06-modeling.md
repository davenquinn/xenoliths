# Thermal modeling of tectonic scenarios

The Farallon Plate, Monterey Plate, and slab window scenarios for the
source of the Crystal Knob xenoliths all imply a peridotite composition
with a depleted (convecting-mantle) isotopic and trace-element
signature.  Though petrographic and geochemical variations provide
information on the depletion history, they cannot discriminate between
these potential depleted convecting mantle sources. However, these
emplacement scenarios present potentially distinct thermal structures
due to large differences in timescales of cooling.

The first set of models, displayed in -@fig:model_results|a 
and @fig:model_tracers|a, correlate to a shallow slab-window
scenario for mantle lithosphere emplacement.
The emplacement of slab-window
asthenosphere directly under the coastal central California crust
entails the truncation of a low-temperature forearc geotherm at 19 Ma
[@Atwater1998] and the substitution of an asthenospheric adiabat below
this level.  The model begins at 24 Ma, corresponding to the time of
opening of the Mendocino slab window under southern California
[@Wilson2005].  The geotherm begins as a steady-state profile to 600 ºC
at 30 km, truncated by a mantle adiabat.  The mantle is held at
asthenospheric conditions for a set period which is varied between model
runs (from 0 to 6 Myr) to simulate a period of active convection, after
which it relaxes conductively to the conclusion of the model.  This
scenario would provide the hottest modern geotherm, and previous
modeling by @Erkan2008 has suggested it yields geotherms too hot to
correspond to the modern regional geotherm.

The second set of models, laid out in
@fig:model_results|b and -@fig:model_tracers|b,
tracks the potential thermal structure of oceanic
plates stalled under the forearc at different times. Models begin at the
subduction time of that oceanic lithosphere parcel and an initial
thermal structure corresponding to the Global Depth and Heat model
[@Stein1992] for oceanic lithosphere for particular age of oceanic
crust. The subduction time and age of oceanic crust covary to represent
different phases of Farallon plate subduction beneath the coast of
Southern California, corresponding to @Seton2012. Thermal conditions
during subduction are tracked using the @Royden1993a steady-state
forearc model. The samples then relax to the present. After subduction
and underplating, the cooled oceanic lithosphere re-equilibrates with an
overlying 30 km of forearc crust until the present, or for our xenolith
samples until the time of ca. 1.7 Ma entrainment and eruption. The
youngest "stalled slab" scenario corresponds to the geologic scenario of
a relict Monterey-plate slab.  However, a series of older cooling
timescales are modeled, representing a wide range of potential timings
for backstepping of the subduction megathrust and underplating of a
slice of mantle lithosphere. Though these represent plausible thermal
histories, only the youngest "Monterey plate" can be explicitly tied to
a geodynamic and geological evidence of subduction instability.

The "Monterey plate" tectonic scenario, as discussed in @sec:discussion,
entails lateral translation on a dipping subduction megathrust. However,
absent of consideration of shear heating (which appears to be minor,
e.g.  @Kidder2013), the thermal scenario can be be reduced to the
subduction of younger oceanic mantle lithosphere. Potential Monterey
Plate mantle lithosphere beneath Crystal Knob would have been emplaced
under the ridge at 27 Ma (corresponding to the chron 7 magnetic anomaly)
and subducted shortly thereafter [@Atwater1998; @Wilson2005]. Due to
slower margin-normal convergence during microplate fragmentation and
rotation [@Wilson2005], the parcel would take ~3 Myr to reach its final
stalled position (~100 km behind the trench) as shown in Figure
@fig:neogene_sections'b. However, for model simplicity, we do not
incorporate this disequilibrium shift in starting conditions.

@fig:model_tracers|c and -@fig:model_results|c shows a set of scenarios
corresponding to the late-Cretaceous underplating scenario envisioned in
@fig:cross_sections. The stalled-slab and late-Cretaceous underplating
scenarios are similar in construction, with initial emplacement beneath
a mid-ocean ridge, and cooling on the seafloor.  The initial conditions
and thermal evolution of this scenario are qualitatively similar to the
older models of **B**, except that this scenario has more geological
constraints. Still, they show much the same thermal structure.

In the Late Cretaceous duplexing scenario, the maximum age of
underplating is 70 Ma, based on the youngest ages of the most pertinent
(Sierra de Salinas and correlative San Emigdio-Rand) schist bodies
[@Barth2003; @Grove2003; @Saleeby2007; @Chapman2010; @Chapman2016].
Seafloor being subducted at that time was 40 Myr old [@Seton2012;
@Liu2010]. This 110 Myr cooling history implies a relatively cold modern
geotherm.  The thermal structure of the forearc is set by thermal
constraints on the temperature of batholithic rocks at 800ºC at 0.75 GPa
at the time of underplating [@Kidder2003].
The resulting geotherm (similar to the steady-state
geotherms without the leading temperature constraint) are subjected to
heating from below by slab window underplating of asthenospheric
material at 80 km depth for a period of 0 to 6 Myr, corresponding to a
deeper version of the underplating in the slab-window scenario.

Given the range of potential geothermal scenarios, models for the
emplacement of depleted mantle lithosphere under the central coastal
California region can be tested by comparison of their implied
geothermal structure with xenolith geothermometry.

<!--[[reconstruction]]-->

<!--[[model_parameters]]-->

## Model setup

To distinguish between potential emplacement mechanisms for the mantle
lithosphere sampled by Crystal Knob, a forward model of the geotherm
implied by each of the tectonic scenarios shown in @fig:neogene_sections
is constructed.  A model based on the one-dimensional heat-flow equation
$$\frac{\partial T}{\partial t} = \frac{k}{\rho C_p} \frac{\partial^2
T}{\partial z^2} + \frac{\alpha}{\rho C_p}$$ {#eq:heat_flow} is used to
track a vertical profile through the lithosphere. This framework is used
to follow the thermal state of the xenolith source region from its most
recent thermal peak, regardless of tectonic setting, to its final
emplacement beneath the Crystal Knob eruption site.

To support this modeling, we use several auxiliary analytical models
from the literature to constrain portions of our modeled scenarios.  We
use the Global Depth and Heat (GDH) model for oceanic crust
[@Stein1992], and the @Royden1993a forearc geotherm model for
subduction.  Standard values are used for oceanic and continental
material properties, and are given in [@tbl:model_parameters].

To simulate subduction and underplating, the forearc geotherm is stacked
atop the modeled oceanic geotherm and relaxed towards the present by
iteratively solving the heat-flow equation using finite differences. The
entire model is implemented in Python, with finite-difference modeling
based on the FiPy software package [@Guyer2009]. Explicit and implicit
finite difference approaches are combined using a two-sweep technique
[@Crank1947] to ensure a stable result.  The model is run to a depth of
500 km to remove the effects of an unknown mantle heat flux.

### Oceanic geotherm

For the Neogene stalled Monterey plate and Late Cretaceous Farallon
mantle nappe scenarios, the Global Depth and Heat (GDH) model
[@Stein1992] is used to trace the thermal evolution of the oceanic
lithosphere from its emplacement at the spreading ridge until
subduction.  This model is a Taylor-polynomial fit of cooling parameters
to global heat-flow and depth datasets. This fit yields higher geotherms
than half-space cooling models that are directly based on @eq:heat_flow
(e.g., @Fowler2005), and tends to produce higher geotherms for old
oceanic lithosphere.  All models, including GDH and half-space cooling
models, significantly overestimate heat flux from young oceanic plates,
a fact that is likely attributable to vigorous hydrothermal circulation
in young submarine lithosphere [@Stein1992;@Stein1995].  This may result
in overestimates of geothermal gradients for the scenarios with the
youngest subducted oceanic crust, such as the Monterey Plate scenario at
the left of @fig:model_tracers.

<!--[[model_tracers]]-->

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

### Underplating

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

In the late Cretaceous underplating scenario, the temperature is pegged
at 715ºC at 25 km depth, a temperature constraint that is established
based garnet-biotite thermometry of exhumed granites of the Sierra de
Salinas [@Ducea2003]. Figure @fig:model_results'c, panel 2 correctly
captures the thermobarometric constraints and inverted metamorphic
gradient recorded by the Pelona schist [@Kidder2006;@Kidder2013] for
this episode of subduction, validating this approach to calculating the
forearc geotherm.

<!--[[cross_sections]]-->

<!--[[neogene_sections]]-->

### Model simplifications

This model framework has several simplifications.  Subducted oceanic
crust is not considered to have distinct thermal properties from the
oceanic mantle.  Increasing the thermal conductivity of the model domain
substantially flattens the modeled geotherms, but does not affect the
relative temperatures predicted by the geotherms.  Additionally, though
there are no reliable estimates of the mantle heat flux that cover the
model domain, the model is run to great depth to avoid any influence of
this uncertainty on the surface geotherm.

The confounding factor of an active subduction zone just outboard of the
scenarios for the older models is also not included within the model.
When the trench interface jumps with the emplacement of an oceanic
mantle nappe beneath the forearc, the new subduction interface will cool
the detached nappe from below. This is not modeled because it would
substantially increase model complexity (requiring a fully iterative
approach to the forearc geotherm), and at this distance (~100 km)
inboard of the final trench interface, there is limited scope for
further episodic rollback after emplacement of the nappe(s) of presumed
xenolith source [e.g. Figure @fig:neogene_sections'c].  Further,
although an active subduction interface at depth will cool the mantle
lithosphere from below, the subduction of progressively younger crust
until cessation at ~27 Ma will gradually increase the heat on the
subduction interface.  The models for these scenarios [@fig:model_comparisons'b and c]
are already near the coolest
permitted by our xenolith constraints.  As these geotherms are already
quite cold, introducing this added complexity will not significantly
change the model results.  However, Farallon and forearc scenarios can
be treated as maximum temperatures because of the influence of the
overriding slab.

Finally, and most significantly, surface erosion after underplating is
taken to be zero. The majority of erosion to the mid-crustal levels now
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

The uncertainties inherent in this model tend to bias the results
towards predicting lower-temperature geotherms over the model domain and
more shallowly sloping geotherms over the mantle lithosphere. This is
especially significant in light of comparisons with measured values of
heat flux and xenolith thermobarometry, which are not subject to these
biases. Thus, geotherms predicted by this model might be underestimates
for potential mantle temperature at a given depth, especially for the
older tectonic scenarios modeled.

<!--[[model_results]]-->


### Model results

Model results are presented as geotherms corresponding to specific model
steps in @fig:model_results and as temperature--time tracers in
@fig:model_comparison.  For the underplating scenario, the @Royden1993a
forearc model predicts low temperatures (~235-245 ºC) at the subduction
interface. This is quite low relative to the temperatures predicted for
the Pelona schist (~700 ºC) by @Kidder2013, or 700-800 ºC derived as an
emplacement constraint for the Sierra de Salinas schist [@Kidder2006].
In the stalled Monterey-plate scenario, temperature is predicted to be
980 ºC at the subduction interface. Despite this uncertainty in
subduction conditions, the model is much more sensitive to the thermal
history of the oceanic plate than to the forearc geotherm. Therefore,
the choice of the relatively cool "GDH" model to track the evolution of
the suboceanic thermal structure for scenarios **B** and **C** is an
important control on the model results.

Despite the pinning of subduction temperatures to the Sierra de Salinas
schist, the baseline late Cretaceous rollback scenario
shown in @fig:model_comparison'c
has a very similar final thermal structure to
the longest-running stalled slab scenarios, reflecting the basic
correspondence of this Cretaceous underplating scenario with a
generalized slab rollback event of similar age.  This also supports the
idea that high subduction-channel temperatures experienced during
late-Cretaceous flat slab subduction and schist metamorphism did not
have a long-lasting impact on the thermal structure of the margin.  We
would expect a deep Miocene slab window event
(depicted in @fig:model_comparison'c)
to have a similar effect on the oldest
scenarios of @fig:model_comparison'b.

The model predicts much higher temperatures within the mantle
lithosphere, and much higher geothermal gradients, for the slab window
than for the Farallon-plate or stalled-slab models. The geothermal
gradients implied for this scenario are much higher than those is
observed in the Coast Ranges.  This corresponds to the model findings of
@Erkan2008. However, these studies concluded that the low heat flows
must be due to a stalled slab, where in fact underplated Farallon mantle
nappes satisfy the surface heat flow data equally well, given a deep
slab window heating event.

The case of relict Farallon-plate material shows low geotherms that
correspond to mantle lithosphere temperature conditions too cold for the
xenolith constraints. However, the Farallon plate with reheating by a
deep slab window in the early Miocene shows results similar to that for
the youngest stalled slab scenarios except for the "Monterey Plate"
scenario. The Monterey Plate scenario matches well with the geothermal
constraints derived from heat flow modeling. However, when potential
temperature overestimates from extrapolation of heat flow values are
considered along with underestimate effects in the modeled geotherms,
the slightly colder temperatures predicted by the reheated relict mantle
lithosphere scenario fall in a reasonable range for the geotherm within
the mantle lithosphere beneath central California. This scenario is thus
equally attractive from a geothermal point of view to explain the
moderately elevated geothermal gradient seen in the mantle lithosphere,
while corresponding to the geologic context much better than the
"stalled slab" scenario.

