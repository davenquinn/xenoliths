# Thermal modeling of tectonic scenarios {#sec:modeling}

The Crystal Knob mantle xenoliths have a peridotite composition with a depleted
(convecting-mantle) isotopic and trace-element signature.  Petrographic and
geochemical variations provide information on the depletion history but cannot
discriminate between slab window, Monterey Plate, and Cretaceous mantle
duplexing origins for the sampled parcel of depleted convecting mantle.
However, these emplacement scenarios present potentially distinct thermal
structures due to large differences in timescales of cooling. Tectonic models
for the emplacement of depleted mantle lithosphere under the central California
coast can be tested by comparison of their implied geothermal structure with
xenolith geothermometry.

## Model setup

To distinguish between potential emplacement mechanisms for the mantle
lithosphere sampled by Crystal Knob, we construct a forward model of the geotherm
implied by each of the tectonic scenarios discussed in @sec:tectonic_scenarios.
A model based on the one-dimensional heat-flow equation
$$\frac{\partial T}{\partial t} = \frac{k}{\rho C_p} \frac{\partial^2 T}{\partial z^2} + \frac{\alpha}{\rho C_p}$$ {#eq:heat_flow}
(e.g. @Turcotte2002, with $T$: temperature, $t$: time, and standard values for oceanic and continental
material properties shown in @tbl:model_parameters) is used to track the
evolution of the lithospheric geotherm predicted by the three tectonic
scenarios presented above.

<!--[[[tbl:model_parameters]]]-->

To simulate both subduction and slab-window driven mantle underplating,
the forearc geotherm is stacked atop a modeled sub-oceanic or asthenospheric
geotherm and relaxed towards the present. The
model is implemented in Python using the FiPy software package [@Guyer2009],
combining explicit and implicit finite difference approaches using a two-sweep
technique [@Crank1947] to ensure a stable result.  The model is run to a depth
of 500 km to remove the effects of unknown mantle heat flux.

A mantle adiabat held at the base of the crust
provides a static initial thermal structure for models of scenario **A**, while
analytical models for the thermal evolution of oceanic crust [@Stein1992]
and a forearc geotherm under continuing subduction [@Royden1993a]
provide time-dependent boundary conditions for scenarios **B** and **C**. More
information about model setup and integration is given in
@sec:model_supplement.

## Model results

Model results are presented as temperature--time tracers in @fig:model_tracers
and as geotherms corresponding to specific model steps in @fig:model_results.

<!--[[[fig:model_tracers]]]-->

<!--[[[fig:model_results]]]-->

### Shallow slab window

The geologic context of the shallow slab window scenario (model group **A**) is
shown in @fig:neogene_sections|a, and thermal modeling results are shown in
@fig:model_tracers|a and -@fig:model_results|a. The model begins at 24 Ma,
corresponding to the opening of the Mendocino slab window under southern
California [@Wilson2005]. A steady-state profile through the crust is truncated
by a mantle adiabat to simulate direct contact with the ascended asthenosphere
(for 0-6 Myr), after which the domain relaxes conductively to the conclusion of
the model. Previous modeling by @Erkan2008 suggests that this scenario yields
temperatures too hot to correspond to the modern regional geotherm. We confirm
this assessment, finding that this scenario produces extremely steep geotherms
at the upper boundary of spinel lherzolite stability for much of the
temperature domain of interest [@fig:model_comparison], reproducing neither the
xenolith pressure--temperature array developed in this study nor the
seismically-inferred depth of the lithosphere-asthenosphere boundary [e.g.
@Li2007].

### Neogene stalled slab

The geologic context of the stalled slab scenario (model group **B**) is shown
in @fig:neogene_sections|b, and modeling results are displayed in
@fig:model_tracers|b and -@fig:model_results|b. This scenario tracks the
potential thermal structure of oceanic plates stalled under the forearc at
a range of times. Each run begins with the subduction of oceanic lithosphere
assigned an initial thermal structure corresponding to oceanic lithosphere of
a given age.

We model cooling scenarios for a wide range of underplating times, with the
start of subduction ranging from 80 to 22 Ma. This reflects the long subduction
history of the Farallon plate beneath the central California coast through the
Cretaceous and Paleogene. These subduction times, T$_\textrm{start}$,  set the
initial conditions shown in @fig:model_tracers|b and the first panel of
@fig:model_results|b. Each model operates on oceanic crust of the appropriate
age for the time of subduction, given the geometry of Farallon plate subduction
over the Cretaceous and Paleogene [@Liu2010; @Seton2012]. As
T$_\textrm{start}$ approaches the present, the age of subducted oceanic crust
generally decreases, reflecting the approach of the Pacific--Farallon spreading
ridge to the western margin of North America.

Stalled slab scenarios with subduction ages older than 30 Ma simulate
rollback during sustained Farallon-plate subduction.
While backstepping of the subduction megathrust and underplating of a slice of
mantle lithosphere could, in principle, occur at any time, these older
stalled-slab models do not correspond to geodynamic and geological evidence of
a specific episode of subduction instability. Though improbable, these models
are included to fully explore the model space between model groups **B** and
**C**, and are represented with a reduced opacity on @fig:model_tracers|b. In
the oldest model with a subduction time of 70 Ma, the oceanic lithosphere is 50
Myr old at the time of subduction. At this time, the Shatsky conjugate had
already subducted to beneath the Cordilleran interior [@Liu2010] and the
Nacimiento belt of the Franciscan was in its later stages of subduction
accretion [@Chapman2016a]. This is the earliest time a stalled slab could have
developed outside of the specific scenario treated in model group **C**.

The youngest model run in @fig:model_tracers|b corresponds to the "Monterey plate"
hypothesis [@Pikser2012; @VanWijk2001], which entails
hypothetical northward lateral translation on a shallowly-dipping
arrested subduction megathrust.
The potential thermal effects of the required anhydrous shearing of the
underplated oceanic lithosphere along a ~300 km flat displacement trajectory
\[see @sec:stalled-slab-bad\] are not accounted for in model **B**. Instead, this
scenario is modeled simply as a young endmember stalled-slab scenario, with
generation of mantle lithosphere beneath the oceanic spreading ridge at 27 Ma
(corresponding to the chron 7 magnetic anomaly) and subduction shortly
thereafter [@Atwater1998; @Wilson2005].

Overall, the stalled-slab underplating scenarios represented in **B** result
in cooler geotherms than shallow slab window
underplating, matching the broad thermobarometric constraints placing
Crystal Knob xenolith entrainment relatively deep within the spinel stability
field [@fig:model_comparison]. The Monterey plate subduction
scenario likewise predicts a modern geotherm that matches the entrainment
constraints on the Crystal Knob xenoliths. Without consideration of
potential bias towards colder measurements in the modeled geotherms,
this appears to match our xenolith data. Accounting for
possible external effects \[@sec:heat-flow and @sec:model_supplement\],
it suggests a hotter geotherm than that derived
from the thermobarometric constraints.

### Late-Cretaceous mantle nappe underplating

The geologic context of the Late Cretaceous mantle nappe underplating scenario
(model group **C**) is shown in @fig:neogene_sections|c, and model results are
displayed in @fig:model_tracers|c and -@fig:model_results|c. The initiation of
this scenario is similar to the older stalled slab scenarios
[@fig:model_tracers|b]. In both cases, the oceanic mantle forms under the
Pacific--Farallon spreading ridge during the early Cretaceous, thermally
matures to form a mantle lithosphere lid during oceanic plate transport, and
subducts beneath the southwest Cordilleran margin later in the Cretaceous.
Thus, the initial conditions and thermal evolution of scenario **C** are
qualitatively similar to the older runs of **B**, except that this scenario
incorporates more crustal geological constraints that pertain to its subduction
history. In model **C**, the @Royden1993a forearc geotherm is tied to
temperature constraint of 715ºC at
25 km depth based on garnet-biotite thermometry of Salinia granites that lie
tectonically above the subduction complex, and ~575ºC at 30 km depth based on
garnet-biotite thermobarometry on the proximally underplated schist of Sierra
de Salinas [@Ducea2003; @Kidder2006]. The subduction conditions and
mantle lithosphere structure implied by this scenario are shown in
@fig:cross_sections.

In model **C**, the age of subduction and underplating is taken as  70 Ma,
based on the youngest mica Ar/Ar ages for the Sierra de Salinas/Nacimiento
Franciscan subduction complex [@Barth2003; @Grove2003; @Saleeby2007;
@Chapman2010; @Chapman2016; @Chapman2016a]. Seafloor being subducted at that
time was 40 Myr old [@Seton2012; @Liu2010]. In this tectonic scenario
\[@fig:neogene_sections|c and @fig:cross_sections\], Farallon oceanic lithosphere
continued to subduct after mantle nappe detachment until the Pacific--Farallon
spreading ridge encountered the trench in the Neogene. In the thermal model
[@fig:model_results], the underplated mantle nappe(s) cool beneath the forearc
for 50 Myr, after which the geotherm is perturbed by the underplating of
asthenosphere at ~80 km depth, corresponding to a deep slab window.

In several model runs, asthenosphere is held against the base of the lithosphere for periods
ranging from 0 Myr to 6 Myr.
An adiabatic temperature gradient with a
mantle potential temperature of 1450ºC is held against the base of the
lithosphere for the duration of contact.
The model for 0 Myr entails instantaneous contact followed immediately
by conductive relaxation, while 6 Myr of sustained upwelling
produces the "kinked" geotherm seen in panel 4 of @fig:model_results|c
at the 18 Ma time step, due to continuing imposition of a mantle adiabat below 80
km depth. A single model without slab window heating
\[highlighted in @fig:model_comparison\] predicts much
cooler geotherms that do not match the mantle geothermal constraints
developed in this study.

@fig:model_results|c, panel 2 shows the thermobarometric constraints
and inverted metamorphic gradient recorded by subduction-channel schists for this episode of
subduction [@Kidder2006; @Kidder2013] and used to tune the @Royden1993a
forearc geotherm model.
These high subduction temperatures constrained by crustal geothemometry make
little difference to the final thermal structure of the mantle
lithosphere [@fig:model_tracers|c]. When not reheated by a deep slab
window, the Cretaceous underplating scenario has a similar final thermal
structure to the longest-running stalled slab scenarios in **B**
[@fig:model_comparison]. This
reflects the model's basic correspondence with a generalized Farallon
plate mantle lithosphere underplating event of similar age. High subduction-channel temperatures
experienced during late-Cretaceous flat slab subduction and schist
metamorphism did not have a long-lasting impact on the thermal structure
of the margin. Thus, heating by a Miocene deep slab window
is required for Cretaceous mantle nappe underplating scenarios to produce warm mantle
lithosphere.

<!--[[[fig:model_comparison]]]-->

## Summary of model results

Our thermal modeling predicts much higher temperatures within the mantle
lithosphere, and much higher geothermal gradients, for the shallow slab window
than for the stalled-slab or underplated mantle nappe models. The geothermal
gradients implied for the shallow slab window scenario are much higher than those
suggested by heat flow data in the Coast Ranges, leading @Erkan2008 to favor a stalled slab
tectonic scenario.
Our modeling predicts that both the stalled slab
and Cretaceous mantle nappes reheated by a deep slab window recover the geotherm determined by
xenolith thermobarometry, while not violating constraints posed by heat
flow data. An assessment of model sensitivity presented in
@sec:model_supplement includes biases that may influence the model
results. Most pertinent is the underestimation of modeled geothermal
gradients due to lack of accounting for exhumation during lithospheric thermal
equilibration. This would: 1. push model results for the slab window scenario
further out of the field of acceptable mantle lithosphere geotherms derived
from xenolith constraints; 2. push the Monterey plate to the upper margin of
the field; and 3. push reheated mantle nappe towards the centroid of
the field. The direction of these potential model biases is summarized in
@fig:model_comparison.

