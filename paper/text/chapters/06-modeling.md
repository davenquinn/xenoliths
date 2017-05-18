# Thermal modeling of tectonic scenarios

The Farallon Plate, Monterey Plate, and slab window scenarios for the
source of the Crystal Knob xenoliths all imply a peridotite composition
with a depleted (convecting-mantle) isotopic and trace-element
signature.  Though petrographic and geochemical variations provide
information on the depletion history, they cannot discriminate between
these potential depleted convecting mantle sources. However, these
emplacement scenarios present potentially distinct thermal structures
due to large differences in timescales of cooling.
Models for the
emplacement of depleted mantle lithosphere under the central coastal
California region can be tested by comparison of their implied
geothermal structure with xenolith geothermometry.

<!--[[reconstruction]]-->

<!--[[model_parameters]]-->

## Model setup

To distinguish between potential emplacement mechanisms for the mantle
lithosphere sampled by Crystal Knob, we construct a forward model of the geotherm
implied by each of the tectonic scenarios **A**, **B**, and **C**
shown in @fig:neogene_sections.  A model based on the one-dimensional heat-flow equation
$$\frac{\partial T}{\partial t} = \frac{k}{\rho C_p} \frac{\partial^2 T}{\partial z^2} + \frac{\alpha}{\rho C_p}$$ {#eq:heat_flow}
is used to track a vertical profile through the lithosphere.
This framework is used to follow the thermal state of the xenolith source region from
subduction (or, in case **A**, underplating beneath the crust) to final
emplacement beneath the Crystal Knob eruption site at 1.65 Ma.

For scenarios **B** and **C**, we simulate subduction and underplating by
stacking the forearc geotherm atop the modeled oceanic geotherm and relaxed towards the present by
iteratively solving the heat-flow equation using finite differences. The
entire model is implemented in Python, with finite-difference modeling
based on the FiPy software package [@Guyer2009]. Explicit and implicit
finite difference approaches are combined using a two-sweep technique
[@Crank1947] to ensure a stable result.  The model is run to a depth of
500 km to remove the effects of unknown mantle heat flux.

Several auxiliary analytical models are used to constrain portions of
our modeled scenarios.  We use the Global Depth and Heat (GDH) model for
oceanic crust [@Stein1992], and the @Royden1993a forearc geotherm model
to model the evolution of a geotherm during subduction on a continuously
subducting model.  Standard values are used for oceanic and continental
material properties, and are given in [@tbl:model_parameters].
We neglect the effects of shear heating by simple down-dip
displacements along the subduction megathrust based on the thermal
modeling of @Kidder2013.
Additional information about model setup and integration is given in @sec:model_supplement.

<!--[[model_tracers]]-->

<!--[[cross_sections]]-->

<!--[[neogene_sections]]-->

<!--[[model_results]]-->

### Model results

Model results are presented as geotherms corresponding to specific model
steps in @fig:model_results and as temperature--time tracers in
@fig:model_tracers.

#### Shallow slab window

Model group **A**, displayed in -@fig:model_results|a 
and @fig:model_tracers|a, shows a shallow slab-window
scenario for mantle lithosphere emplacement.
The model begins at 24 Ma, corresponding to the time of
opening of the Mendocino slab window under southern California
[@Wilson2005]. A steady-state profile through the crust is truncated
by a mantle adiabat to simulate direct contact with the asthenosphere
(for 0-6 Myr), after
which the domain relaxes conductively to the conclusion of the model.
Previous
modeling by @Erkan2008 suggests that this scenario yields geotherms too hot to
correspond to the modern regional geotherm.
We confirm this assessment, finding that these scenarios produce extremely
"hot" geotherms that are above the stability of spinel lherzolite for
much of the temperature domain of interest [@fig:model_comparison].

#### Stalled slab

Model group **B**, displayed in
@fig:model_results|b and -@fig:model_tracers|b,
tracks the potential thermal structure of oceanic
plates stalled under the forearc at successive times. Each run begins
at a specified time with the subduction of oceanic lithosphere
assigned an initial
thermal structure corresponding to the Global Depth and Heat model
[@Stein1992] for oceanic lithosphere of a given age of oceanic
crust.

<comment>Track the entire model run then at the end of this section cover the
Monterey plate case</comment>

The "Monterey plate" scenario is a subset of these models entailing
hypothetical northward lateral translation on a shallowly-dipping subduction megathrust.
Neglecting shear heating (which appears to be minor, e.g.  @Kidder2013),
this scenario can be modeled as a young
endmember stalled-slab scenario, and is shown as the youngest model of
**B**. Potential Monterey
Plate mantle lithosphere beneath Crystal Knob would have been generated beneath the oceanic spreading ridge at 27 Ma (corresponding to the chron 7 magnetic anomaly)
and subducted shortly thereafter [@Atwater1998; @Wilson2005].

<comment>Move this up</comment>
In addition to the Monterey plate scenario, a series of older cooling
scenarios are modeled, representing a wide range of potential timings
for backstepping of the subduction megathrust and underplating of a
slice of mantle lithosphere.
Covarying subduction time and age of oceanic crust are
constrained by @Seton2012 and represent
different phases of Farallon plate subduction beneath the coast of
Southern California.
Though these scenarios represent plausible thermal
histories, only the "Monterey plate" construction can be tied to
geodynamic and geological evidence of a specific episode of subduction instability.

These scenarios result in cooler geotherms than the shallow slab window
underplating, matching the broad thermobarometric constraints on Crystal Knob xenolith entrainment relatively deep within the spinel stability field [@fig:model_comparison]. The Monterey plate subduction
scenario predicts a modern geotherm that coincides with the entrainment
constraints on the Crystal Knob xenoliths.

#### Late-Cretaceous stalled slab

@fig:model_tracers|c and -@fig:model_results|c shows a set of scenarios
corresponding to the late-Cretaceous underplating scenario envisioned in
@fig:cross_sections. These scenarios are similar in construction to **B**
with initial formation at the mid-ocean ridge, and cooling within the oceanic
lithosphere thereafter. The initial conditions
and thermal evolution of this scenario are qualitatively similar to the
older models of **B**, except that this scenario has more geological
constraints. Still, they show much the same thermal structure.

In the Late Cretaceous duplex scenario, the maximum age of
subduction and underplating is 70 Ma, based on the youngest ages of the most pertinent
(Sierra de Salinas and correlative San Emigdio-Rand) schist bodies
[@Barth2003; @Grove2003; @Saleeby2007; @Chapman2010; @Chapman2016].
Seafloor being subducted at that time was 40 Myr old [@Seton2012; @Liu2010].
This 110 Myr cooling history implies a relatively cold modern
geotherm.
After a long history of cooling beneath the forearc, these geotherms
are subjected to
heating from below by underplating of asthenospheric
material at 80 km depth for a period of 0 to 6 Myr, corresponding to a
deeper version of the slab-window underplating modeled in **A**.

In this set of scenarios, the @Royden1993a
subduction model is tied to temperature constraint of 715ºC at 25 km
depth for garnet-biotite thermometry of exhumed granites of the Santa
Lucia range [@Ducea2003], and thermobarometric constraints on the Sierra
de Salinas schist [@Kidder2006]. Figure @fig:model_results|c, panel 2 correctly captures the
thermobarometric constraints and inverted metamorphic gradient recorded
by subduction-channel schists for this episode of
subduction [@Kidder2006; @Kidder2013], validating our approach to calculating the forearc
geotherm.

These lithologically-constrained high subduction temperatures make
little difference to the final thermal structure of the mantle
lithosphere [@fig:model_tracers|c]. When not reheated by a deep slab
window, the Cretaceous underplating scenario has a similar final thermal
structure to the longest-running stalled slab scenarios in **B**. This
reflects the model's basic correspondence with a generalized slab
rollback event of similar age. High subduction-channel temperatures
experienced during late-Cretaceous flat slab subduction and schist
metamorphism did not have a long-lasting impact on the thermal structure
of the margin. Thus, underplating by a deep slab window during the
Miocene is required for these scenarios to produce warm mantle
lithosphere.

## Model sensitivity and bias

Generally, changes in model parameters do not impact the relative
results for modeled scenarios, due to the consistent lithologic
architecture of the model domain.

Due to widely varying timescale of equilibration for modeled scenarios
in groups **B** and **C**, the model is sensitive to assumptions
about steady-state cooling of the oceanic mantle lithosphere.
The choice of the "GDH" model to track the evolution of
the suboceanic thermal structure is important control on the scale of
temperature variation in @fig:model_tracers|b.
Though GDH is well-calibrated, oceanic cooling models tend to overestimate the heat flow from
young oceanic plates [@Stein1995], potentially yielding higher temperatures
for the younger scenarios of **B**, including
the Monterey plate scenario.

Another key confounding factor not modeled for the subduction scenarios **B** and
**C** is the effects of continued subduction outboard of the model
domain. After rollback and underplating of the modeled section of
oceanic mantle lithosphere, a downgoing slab at depth will tend to cool
the forearc lithosphere from below However, this effect should
diminish over time due to the subduction of younger, hotter oceanic
material [@Royden1993a] and be overprinted by the underplating of hot
slab window material in **C**.

Surface erosion is not modeled, but may bias the results. Any erosion will
result in higher apparent heat flow values and increased geotherm
convexity, as heat is advected from the
top of the model domain by material removal [@Mancktelow1997;@England1990].
Geologic constraints suggest that 15-20 km of erosion
is likely to have occurred in a major pulse of
unroofing coincident with flat-slab underplating and rollback in the
Cretaceous [@Saleeby2003; @Chapman2012], and is thus likely to disproportionately
affect the older models. The lack of erosion in the model framework
biases towards predicting lower geothermal gradient overall.

The uncertainties inherent in this model bias the results
towards predicting lower-temperature,
less-convex geotherms over the model domain.
These potential biases are significant when
making comparisons with measured values of
heat flux and xenolith thermobarometry [e.g. @fig:model_comparison], which are not subject to these
biases. Thus, geotherms predicted by this model might be underestimates
for potential mantle temperature at a given depth, especially for the
older tectonic scenarios modeled.
Additional discussion of these factors can be found in
@sec:model_supplement.

### Summary of model results

The model predicts much higher temperatures within the mantle
lithosphere, and much higher geothermal gradients, for the slab window
than for the late-Cretaceous rollback or stalled-slab models. The geothermal
gradients implied for this scenario are much higher than those is
observed in the Coast Ranges, and the Monterey Plate scenario matches
well with the geothermal
constraints derived from heat flow modeling.
This corresponds to the model findings of
@Erkan2008. However, these studies concluded that the low heat flows
must be due to a stalled slab, where in fact underplated Farallon mantle
nappes satisfy the surface heat flow data equally well, given a deep
slab window heating event.

In scenario **C**, relict Farallon-plate material shows low geotherms that
correspond to mantle lithosphere temperature conditions too cold for the
Crystal Knob xenolith constraints. However, when reheated by a
deep slab window in the early Miocene, this scenario
shows results similar to that for
the youngest stalled slab scenarios in **B** except for the "Monterey Plate"
scenario.

When potential
temperature overestimates from extrapolation of heat flow values
[@sec:heat-flow] are considered along with biases in model geotherms,
the slightly colder temperatures predicted by the reheated relict mantle
lithosphere scenario also fall in a reasonable range for the geotherm within
the mantle lithosphere beneath central California. This scenario thus
provides an equally attractive geothermal gradient to explain the
moderately elevated temperatures seen in the mantle lithosphere,
while fitting the geologic context much better than the
"stalled slab" scenario.

