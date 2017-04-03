# Thermal modeling of tectonic scenarios

The Farallon Plate, Monterey Plate, and slab window scenarios for
the source of the Crystal Knob xenoliths all imply a peridotite composition with a
depleted (convecting-mantle) isotopic and trace-element signature.
Though petrographic and geochemical variations provide information
on the depletion history, they cannot discriminate between these
potential depleted convecting mantle sources. However, these emplacement
scenarios present potentially distinct thermal structures due to
large differences in timescales of cooling.

The Farallon-- and Monterey--plate scenarios are qualitatively similar,
with initial emplacement beneath a mid-ocean ridge, and cooling on the seafloor. After
subduction and underplating, the cooled oceanic lithosphere
re-equilibrates with an overlying 30 km of forearc crust until the
present, or for our xenolith samples until the time of ca. 1.7 Ma entrainment and
eruption. However, the timescales of cooling are significantly different. In
the Farallon-plate scenario, the maximum age of underplating is 70 Ma,
based on the youngest ages of the most pertinent (Sierra de Salinas and
correlative San Emigdio-Rand) schist bodies
[@Barth2003; @Grove2003; @Saleeby2007; @Chapman2010; @Chapman2016].
Seafloor being subducted at that time was 40 Myr old
[@Seton2012; @Liu2010]. This 110 Myr cooling history implies a relatively cold
modern geotherm. The potential Monterey Plate mantle lithosphere would have
been emplaced under the ridge at 27 Ma (corresponding to the chron 9
magnetic anomaly) and subducted shortly thereafter [@Atwater1998; @Wilson2005],
leaving a much shorter period for relaxation of the geotherm. The
emplacement of slab-window asthenosphere directly under the coastal
central California crust entails
the truncation of a low-temperature forearc geotherm at 19 Ma
[@Atwater1998] and the substitution of an asthenospheric adiabat below
this level. This scenario would provide the hottest modern geotherm,
which, according to @Erkan2008, is too hot to correspond to the
modern regional geotherm. <!-- (Daven, are they referring to the region
under CRTA, or the cooler Great Valley and Sierra Nevada) -->

<!--[[reconstruction]]-->

<!--[[model_parameters]]-->

## Model setup

To distinguish between potential emplacement mechanisms for the mantle
lithosphere sampled by Crystal Knob, a forward model of the geotherm
implied by each of the tectonic scenarios shown in @fig:neogene_sections
is constructed.
A model based on the one-dimensional heat-flow equation
\begin{equation}
\frac{\partial T}{\partial t} = \frac{k}{\rho C_p} \frac{\partial^2
T}{\partial z^2} + \frac{\alpha}{\rho C_p} \label{eqn:heat-flow}
\end{equation}
is used to track a vertical profile through the
lithosphere. This framework is used to follow the thermal state of the
xenolith source region from its most recent thermal peak, regardless
of tectonic setting, to its final emplacement beneath the Crystal Knob eruption site.

To support this modeling, we use several auxiliary analytical models
from the literature to constrain portions of our modeled scenarios.
We use the Global Depth and Heat (GDH) model for oceanic crust
[@Stein1992], and the @Royden1993a forearc geotherm model for
subduction.
Standard values are used for oceanic and continental material
properties, and are given in [@tab:model_parameters].

Given the range of potential geothermal scenarios, models for the
emplacement of depleted mantle lithosphere under the central coastal
California region can
be tested by comparison of their implied geothermal structure with xenolith
geothermometry.

### Oceanic geotherm

For the Neogene stalled Monterey plate and Late Cretaceous Farallon mantle nappe scenarios, the Global Depth and Heat (GDH)
model [@Stein1992] is used to trace the thermal evolution of the oceanic
lithosphere from its emplacement at the spreading ridge until subduction.
This model is an Taylor-polynomial fit of cooling parameters to global
heat-flow and depth datasets. This fit yields higher geotherms than half-space
cooling models that are directly based on Equation \eqn{heat-flow}
(e.g., @Fowler2005), and tends to produce higher geotherms for old
geothermal lithosphere.
All models, including GDH and half-space cooling models, significantly
overestimate heat flux from young oceanic plates, a fact that is likely attributable
to vigorous hydrothermal circulation in young submarine lithosphere [@Stein1992;@Stein1995].
This may result in overestimates of geothermal gradients for the youngest
subduction scenarios.

<!--[[model_tracers]]-->

### Supra-subduction geotherm

The geotherm of the forearc wedge during subduction is calculated using
the @Royden1993a analytical solution for the steady-state thermal
structure of continuously-subducting systems.  <!-- At this rate it takes 5 Myr after
subduction to reach the final position! This is pretty significant, it
seems..., maybe should be incorporated! Also, depth of subduction
interface may be greater, especially in Monterey-plate (i.e. probably
not flat-slab case). --> Shear heating on the subduction thrust is taken
to be 15 mW/m^2. Rates of surface erosion in the forearc and
subduction accretion are taken to be 0. <!-- Accretion rates of 0.2-3.6
km/Myr favored by Kidder,2013 based on Sierra de Pelona schist. -->

The coastal California accretionary crust is represented homogenously as a material with a
thermal conductivity of 2.71 W/m/K, specific heat capacity of
1000 J/kg/K, density of 2800 kg/m^3 and a radiogenic heat
flux of 2 uW/m^3, values that are close to average for the
continental crust [@Fowler2005] and those used by @Kidder2013 to model
the thermal conditions along the Late Cretaceous shallow subduction
megathrust segment.
2 uW/m^3 for radiogenic heat production in the crust
is actually a relatively conservative estimate given the fluxes implied for
Sierra Nevada batholithic material by @Brady2006, and the fact that much of the
subduction channel material is pelitic sediment rich in radiogenic elements
<comment>should put some reference to Franciscan radiogenic heat or just
pelitic sediments</comment>.
<!-- Check Kidder2013 and Brady2006 -->

### Underplating

To simulate subduction and underplating, the forearc geotherm
is stacked atop the modeled oceanic geotherm and relaxed towards
the present by iteratively
solving the heat-flow equation using finite differences. The entire
model is implemented in Python, with finite-difference modeling based on
the FiPy software package [@Guyer2009]. Explicit and implicit finite
difference approaches are combined using a two-sweep Crank-Nicholson
technique [@Crank1947] to ensure a stable result.

Progressive subduction of the downgoing slab beneath the
forearc wedge is modeled as stepwise advection beneath a linearly thickening
forearc wedge conforming to the @Royden1993a thermal model using
the parameters outlined above.
For all cases, the final depth of the underplated subduction interface
is taken to be 30 km, and the distance landward of the subduction zone
is taken to be 100 km.
No effort is made to differentiate 'flat-slab' and baseline subduction
geometries. Though increasing the slab dip angle will result in a cooler subduction interface at a given depth, the
overall effect on the evolution of the thermal
scenarios appears to be minimal.

In the Farallon-plate scenario, the temperature is pegged at 715ºC at
25 km depth, a temperature constraint that is established based garnet-biotite
thermometry of exhumed granites of the Sierra de Salinas.
Figure \ref{model_results}C, panel 2 correctly captures the inverted metamorphic
gradient found by @Kidder2006 for this episode of subduction,
validating this approach to calculating the forearc geotherm.



<!-- @Groome2006: ridge subduction modeling -->

<!--[[cross_sections]]-->

<!--[[neogene_sections]]-->

### Model simplifications

This model framework has several simplifications.
Surface erosion after underplating is taken to be zero. The majority of
erosion to the mid-crustal levels now at the surface in Salinia is
likely to have occurred in a major pulse of unroofing coincident with
flat-slab underplating and rollback [@Saleeby2003; @Chapman2012], and is thus likely to
disproportionately affect the older models. The lack of erosion
in the model framework will likely bias the results to lower geothermal
gradients overall, as advection of material upwards increases the
geothermal gradient. <comment>Shift everything up by an appropriate
amount</comment>.

The confounding factor of an active subduction zone just outboard of the
scenarios for the older models is also not treated.
All of the rollback underplating scenarios are potentially beset by this problem.
When the trench interface jumps with the emplacement of an oceanic mantle
nappe beneath the forearc, the new subduction interface will cool the
detached nappe from below. This is not modeled because it would
substantially increase model complexity (requiring a fully
iterative approach to the forearc geotherm), and at this
distance (~100 km) inboard of the final trench interface, there is
limited scope for further episodic rollback after emplacement of the
nappe(s) of presumed xenolith source.

The subduction zone will have the effect of cooling the
mantle lithosphere from below for the cases in which subduction is
modeled [@fig:model_comparisons\ b and c], which are already near
the coolest permitted by our xenolith constraints.
However, the subduction of progressively younger crust until
the shutoff at ~27 Ma will gradually increase the heat on the bottom of the lithosphere.
As these geotherms are already quite cold, introducing this added complexity will not
significantly change the model results. <comment>Not sure if this makes sense...</comment>

For simplicity, subducted oceanic crust is not considered to have distinct thermal
properties from the oceanic mantle.
Increasing the thermal conductivity of the model domain substantially
flattens the modeled geotherms, but does not affect the relative
temperatures predicted by the geotherms.

<comment>Need to reword this</comment>
There are no reliable estimates of the mantle heat flux that cover the model
domain, and the thermal environment for underplated mantle lithosphere is complicated
by the presence of a subducting slab below the model domain at some depth. The model
is run to great depth to avoid any influence on the surface geotherm. However,
Farallon and forearc scenarios can be treated as maximum temperatures because of
the influence of the overriding slab.

<comment>
Model-predicted heat flows lower than measured values could be explained
by erosion [@Mancktelow1997;@England1990].
</comment>

<!--[[model_results]]-->


### Model results

Model results are presented as geotherms corresponding to specific model steps in @fig:model_results
and as temperature--time tracers in @fig:model_comparison.
For the underplating scenario, the @Royden1993a forearc model
predicts low temperatures (~235-245 ºC) at the subduction
interface. This is quite low relative to the temperatures predicted for
the Pelona schist (~700 ºC) by @Kidder2013, or
700-800 ºC derived as an emplacement constraint for the Sierra de
Salinas schist [@Kidder2006]. In the stalled
Monterey-plate scenario, temperature is predicted to be
980 ºC at the subduction interface. Despite this uncertainty in subduction conditions, the
model is much more sensitive to the thermal history of the oceanic plate
than to the forearc geotherm. Therefore, the choice of the relatively cool "GDH" model to
track the evolution of the suboceanic thermal structure for scenarios **B** and **C**
is an important control on the model results.

Despite the pinning of subduction temperatures to the Sierra de Salinas schist, the
baseline late Cretaceous rollback scenario shown in Figure \ref{model_comparison}c
has a very similar final thermal structure to the longest-running stalled slab scenarios,
reflecting the basic correspondence of this Cretaceous underplating scenario with a
generalized slab rollback event of similar age.
This also supports the idea that high subduction-channel temperatures
experienced during late-Cretaceous flat slab
subduction and schist metamorphism did not have a long-lasting impact on the
thermal structure of the margin.
We would expect a deep Miocene slab window event (depicted in Figure
\ref{model_comparison}c) to have a similar effect on the oldest scenarios of Figure \ref{model_comparison}b.

The model predicts much higher temperatures within the mantle lithosphere, and
much higher geothermal gradients, for the slab window than for the
Farallon-plate or stalled-slab models. The geothermal gradients implied for
this scenario are much higher than those is observed in the Coast Ranges.
This corresponds to the model findings of @Erkan2008. However, these studies
concluded that the low heat flows must be due to a stalled slab, where in fact
underplated Farallon mantle nappes satisfy the surface heat flow data equally
well, given a deep slab window heating event.

The case of relict Farallon-plate material shows low geotherms that correspond to
mantle lithosphere temperature conditions too cold for the xenolith constraints.
However, the Farallon plate with reheating by a deep slab window in the early Miocene
shows results similar to that for the youngest stalled slab scenario modeled. This
means that the thermal structures of a "Monterey Plate" and a deep slab window scenario
are indistinguishable from a geothermal perspective. Thus, this scenario
is equally attractive from a geothermal point of view to explain a moderately elevated
geothermal gradient in the mantle lithosphere (which is what we see from the heat flow and
xenolith constraints on the geotherm), while corresponding to the geologic
context much better than the "stalled slab" scenario.

