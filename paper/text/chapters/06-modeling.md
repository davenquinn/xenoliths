# Thermal modeling of tectonic scenarios

The Farallon Plate, Monterey Plate, and slab window scenarios for the
source of the Crystal Knob xenoliths all imply a peridotite composition
with a depleted (convecting-mantle) isotopic and trace-element
signature.  Though petrographic and geochemical variations provide
information on the depletion history, they cannot discriminate between
these potential depleted convecting mantle sources. However, these
emplacement scenarios present potentially distinct thermal structures
due to large differences in timescales of cooling.
Tectonic models for the
emplacement of depleted mantle lithosphere under the central coastal
California region can be tested by comparison of their implied
geothermal structure with xenolith geothermometry.

<!--[[reconstruction]]-->

<!--[[model_parameters]]-->

## Model setup

To distinguish between potential emplacement mechanisms for the mantle
lithosphere sampled by Crystal Knob, a forward model of the geotherm
implied by each of the tectonic scenarios
shown in @fig:neogene_sections is constructed.
A model based on the one-dimensional heat-flow equation
$$\frac{\partial T}{\partial t} = \frac{k}{\rho C_p} \frac{\partial^2 T}{\partial z^2} + \frac{\alpha}{\rho C_p}$$ {#eq:heat_flow}
is used to track the evolution of the lithospheric geotherm predicted by
the three tectonic scenarios presented above.

To simulate both subduction and slab-window driven mantle underplating,
the forearc geotherm is stacked atop modeled oceanic (or asthenospheric)
geotherms and relaxed towards the present by
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
More information about model setup and integration is given in @sec:model_supplement.

<!--[[model_tracers]]-->

<!--[[cross_sections]]-->

<!--[[neogene_sections]]-->

<!--[[model_results]]-->

### Model results

Model results are presented as geotherms corresponding to specific model
steps in @fig:model_results and as temperature--time tracers in
@fig:model_tracers.

#### Shallow slab window

The geologic context of the shallow slab window scenario is shown in
@fig:neogene_sections|a, and our thermal modeling for this scenario
(model group **A**) is displayed in @fig:model_results|a
and -@fig:model_tracers|a.
The model begins at 24 Ma, corresponding to the time of
opening of the Mendocino slab window under southern California
[@Wilson2005]. A steady-state profile through the crust is truncated
by a mantle adiabat to simulate direct contact with the ascended asthenosphere
(for 0-6 Myr), after
which the domain relaxes conductively to the conclusion of the model.
Previous
modeling by @Erkan2008 suggests that this scenario yields geotherms too hot to
correspond to the modern regional geotherm.
We confirm this assessment, finding that this scenario produces extremely
"hot" geotherms that are at the upper boundary of spinel lherzolite stability for
much of the temperature domain of interest [@fig:model_comparison],
reproducing neither the xenolith geotherm determined in this
study nor the seismically-determined depth of the
lithosphere-asthenosphere boundary [e.g. @Li2007].

#### Stalled slab

The geologic context of the stalled slab scenario is shown in
@fig:neogene_sections|b, and our thermal modeling of this scenario
(model group **B**) is displayed in @fig:model_results|b and -@fig:model_tracers|b.
This scenario tracks the potential thermal structure of oceanic
plates stalled under the forearc at a range of times. Each run begins at
a specified time with the subduction of oceanic lithosphere assigned an
initial thermal structure corresponding to the Global Depth and Heat model
[@Stein1992] for oceanic lithosphere of a given age of oceanic crust.

We model cooling scenarios for a wide range of underplating times,
reflecting the long subduction history of the Farallon plate beneath the
central California coast through the Cretaceous and Paleogene.
In principle, backstepping of the subduction megathrust and underplating of a
slice of mantle lithosphere could have occurred at any time during this
history. However, only the oldest and youngest stalled slab models correspond
to geodynamic and geological evidence of a specific episode of
subduction instability.

We model a series of scenarios with differently-timed underplating
events, with the start of subduction ranging from 22 to 80 Ma.
These subduction times, T$_\textrm{start}$,  set the beginning of the models shown in
@fig:model_tracers|b and are shown in the first panel of
@fig:model_results|b.
Each model operates on oceanic crust of the appropriate age for the
time of subduction, given the geometry of Farallon plate subduction over
the Cretaceous and Paleogene [@Liu2010; @Seton2012].
As the subduction time moves towards the present, the age of subducted
oceanic crust generally decreases, reflecting the approach of the
Pacific--Farallon spreading ridge to the western margin of North America.
In the oldest model with a subduction time of 80 Ma, the oceanic lithosphere at the time of subduction
is 60 myr old, meaning that the oceanic crust in this model was
generated beneath the Pacific--Farallon spreading ridge at 140 Ma.

Stalled slab scenarios with subduction ages as young as 30 Ma (all but
the last scenario presented on @fig:model_tracers|b) model
rollback during sustained Farallon-plate subduction.
The final model run in @fig:model_tracers|b corresponds to the "Monterey plate"
hypothesis [@Pikser2012; @VanWijk2001], which entails
hypothetical northward lateral translation on a shallowly-dipping stalled subduction megathrust.
The potential thermal effects of the required anhydrous shearing of the underplated
oceanic lithosphere along a ~300 km flat displacement trajectory [@fig:context]
are not accounted for in model **B**. Instead, this scenario
is modeled simply as a young
endmember stalled-slab scenario, with the generation of mantle lithosphere
beneath the oceanic spreading ridge at 27 Ma (corresponding to the chron 7
magnetic anomaly) and subduction shortly thereafter [@Atwater1998; @Wilson2005].

Overall, the stalled-slab underplating scenarios represented in **B** result
in cooler geotherms than the shallow slab window
underplating, matching the broad thermobarometric constraints placing
Crystal Knob xenolith entrainment relatively deep within the spinel stability
field [@fig:model_comparison]. The Monterey plate subduction
scenario likewise predicts a modern geotherm that coincides with the entrainment
constraints on the Crystal Knob xenoliths. Without consideration of
potential bias towards colder measurements in the modeled geotherms,
this appears to be the best model. When accounting for
possible external effects [@sec:model_bias], it may predict a hotter geotherm than derived
from the thermobarometric constraints.

#### Late-Cretaceous mantle nappe underplating

The geologic context of the Late Cretaceous mantle nappe underplating scenario
is shown in @fig:neogene_sections|c, and our thermal modeling of this
scenario (model group **C**) is displayed in
@fig:model_tracers|c and -@fig:model_results|c.
This scenario initiates in a similar fashion to the model runs for the
stalled slab scenario [@fig:model_tracers|b] with the oldest emplacement
ages. In both cases, the oceanic mantle forms under the
Pacific--Farallon spreading ridge during the Late Cretaceous, thermally
matures to form a mantle lithosphere lid during oceanic plate transport,
and subducts beneath the southwest Cordilleran margin later in the
Cretaceous.
Thus, the initial conditions and thermal evolution of scenario **C** are
qualitatively similar to the
older models of **B**, except that this scenario incorporates more
crustal geological constraints that pertain to its subduction history.
In model **C**, the @Royden1993a
forearc geotherm is tied to temperature constraint of 715ºC at 25 km
depth based on garnet-biotite thermometry of Salinia granites that lie
tectonically above the subduction complex, and ~575ºC at 30 km depth
based on garnet-biotite thermobarometry on the proximally underplated
schist of Sierra de Salinas schist [@Ducea2003b; @Kidder2006]. The
subduction conditions and mantle lithosphere structure implied by this
scenario are shown in @fig:cross_sections.

In model **C** the maximum age of
subduction and underplating is taken as ~70 Ma, based on the youngest
ages of the Sierra de Salinas/Nacimiento Franciscan subduction complex
[@Barth2003; @Grove2003; @Saleeby2007; @Chapman2010; @Chapman2016].
Seafloor being subducted at that time was 40 Myr old [@Seton2012; @Liu2010].
In this tectonic scenario [@fig:neogene_sections|c and @fig:cross_sections],
Farallon oceanic lithosphere continued to subduct after mantle nappe
detachment until the Pacific--Farallon spreading ridge encountered the
trench in the Neogene. In the thermal model [@fig:model_results], the
underplated mantle nappe(s) cool beneath the forearc for 50 Myr, and
then the geotherm is perturbed by the underplating of asthenosphere
by an ~80 km deep slab window. We present models with asthenosphere with
an adiabatic temperature gradient held against the base of the
lithosphere for periods ranging from 0 Myr (instantaneous contact
followed immediately by conductive relaxation) to 6 Myr. The model
for 6 Myr of sustained upwelling at the base of the lithosphere
produces the "kinked" geotherm seen in panel 4 of @fig:model_results|c
at the 18 Ma time step, due to imposition of a mantle adiabat below 80
km depth. A single model without slab window heating
[highlighted in @fig:model_comparison] predicts much
cooler geotherms that do not match the mantle geothermal constraints
developed in this study.

Figure @fig:model_results|c, panel 2 shows the thermobarometric constraints
and inverted metamorphic gradient recorded by subduction-channel schists for this episode of
subduction [@Kidder2006; @Kidder2013] and used to tune the @Royden1993
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
young oceanic plates [@Stein1995]. This suggests that the high
geothermal temperatures predicted for the younger stalled slab scenarios
in model group **B**, including the Monterey plate scenario, may be
overestimates.

Another potential confounding factor affecting the older scenarios
of **B** and **C** is the thermal effects of continued subduction
beneath the underplated mantle nappes. After rollback and underplating of the modeled section of
oceanic mantle lithosphere, a downgoing slab at depth could, depending
on its age, cool the forearc lithosphere from below.
However, this effect is considered minimal and
diminishes over time due to the progressive subduction of younger, hotter oceanic
lithosphere.
Reconstruction of the Pacific--Farallon spreading ridge history show
progressively younger oceanic lithosphere entering the southwest
Cordilleran subduction zone between ca. 70 and 30 Ma at a rate of ~-1
Myr/Ma [@Atwater1998; @Liu2009; @Seton2010]. This factor coupled with
slab window emplacement starting at ca. 24 Ma leads to the
interpretation that cooling from below by continued subduction
was of second-order significance.

Surface erosion is not modeled, but may bias the results. Any erosion will
result in higher apparent heat flow values and increased geotherm
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
Additional discussion of these factors can be found in
@sec:model_supplement.

### Summary of model results

Our thermal modeling predicts much higher temperatures within the mantle
lithosphere, and much higher geothermal gradients, for the shallow slab window
than for the stalled-slab or underplated mantle nappe models. The geothermal
gradients implied for the shallow slab window scenario are much higher than those
suggested by heat flow data in the Coast Ranges, leading @Erkan2008 to favor a stalled slab
tectonic scenario.
Our modeling predicts that both the stalled slab and (deep slab window reheated)
Cretaceous mantle nappe scenarios recover the geotherm determined by
xenolith thermobarometry, while not violating constraints posed by heat
flow data.

Exhumation/erosion, while not accounted for in our models,
pushes the modeled geotherm for the shallow slab window
scenario outside of the limit of the thermobarometric constraints on xenolith
entrainment, while pushing the Monterey plate endmember stalled-slab
scenario towards the upper limit of this field, and aligns the reheated
mantle nappe scenario with the center of the field. Unfortunately, we
are prevented from incorporating the effects of exhumation/erosion
due to the lack of temporally-defined geologic constraints on these
processes that can be properly posed within the context of such
modeling.

