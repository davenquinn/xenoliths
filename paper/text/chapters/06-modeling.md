
- Model setups  corresponding to tectonic scenarios
- Model the relaxation of the geotherm during subduction and underplating

### Setups



- Global Depth and Heat model for oceanic crust
- Forearc geotherm model [@Royden1993]
- Standard values for oceanic and continental material properties
- We ignore the effects of a downgoing slab below
<!-- (Not quite sure in what context you are referring to here) -->
    - may be significant over long timescales
    - will generally serve only to cool geotherms


Given the range of potential geothermal scenarios, models for the
emplacement of depleted mantle lithosphere under the central coastal
California region can
be tested by comparison of their implied geothermal structure with xenolith
geothermometry. However, this analysis is a crude approximation due to a lack of well-constrained geobarometers for spinel
peridotites.

<!--[[model_setups]]-->

## Model setup

Evaluation of potential thermal scenarios sampled by Crystal Knob require constraints on the implied present geotherm.
Forward-modeling of the initial thermal conditions will help assess the
level of separation between the scenarios after 25 Myr or more of
re-equilibration beneath the continental margin.
To distinguish between potential emplacement mechanisms for this mantle
lithosphere, a forward model of the geotherm implied by each case is
constructed.
A model based on the one-dimensional heat-flow equation
\begin{equation}
\frac{\partial T}{\partial t} = \frac{k}{\rho C_p} \frac{\partial^2
T}{\partial z^2} + \frac{\alpha}{\rho C_p} \label{eqn:heat-flow}
\end{equation}
is used to track a vertical profile through the
lithosphere. This framework is used to follow the thermal state of the
xenolith source region from its most recent thermal peak, regardless
of tectonic setting, to its final emplacement beneath the Crystal Knob eruption site.

<!-- A temperature of 1300\degC is used to define the thickness of the
lithosphere (this probably doesn't matter because it is simply used to
set parameters for Royden model. Maybe should use mantle adiabat as in
Erkan2009 -->

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

<!-- Could potentially use a more nuanced model, e.g., GDH, or run
finite-difference ourselves -->

For simplicity, oceanic crust is not considered
separately within the model framework.

Increasing the thermal conductivity of the model domain substantially
flattens the modeled geotherms.

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
subduction channel material is pelitic sediment rich in radiogenic elements <comment>should put some reference to Franciscan radiogenic heat</comment>.
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
scenarios appears to be minimal. <!-- is this enough? -->

In the Farallon-plate scenario, the temperature is pegged at 715ºC at
25 km depth, a temperature constraint that is established based garnet-biotite
thermometry of exhumed granites of the Sierra de Salinas.
Figure \ref{model_results}C panel 2 correctly captures the inverted metamorphic
gradient found by @Kidder2006, validating this approach to calculating the
forearc geotherm.



<!-- @Groome2006: ridge subduction modeling -->

<!--[[cross_sections]]-->

<!--[[neogene_sections]]-->

### Limitations of the model

This model framework has several simplifications.
Surface erosion after underplating is taken to be zero. The majority of
erosion to the mid-crustal levels now at the surface in Salinia is
likely to have occurred in a major pulse of unroofing coincident with
flat-slab underplating and rollback [@Chapman2012].
<!-- Would it be helpful to explore the parameter space
fully using Monte Carlo methods
similar to those used by Kidder, 2013? -->
Also, the underplating scenario is modeled incompletely --
when the trench interface jumps with the emplacement of an oceanic mantle
nappe beneath the forearc, the new subduction interface will cool the
detached nappe from below. This is not modeled because it would
substantially increase model complexity (requiring a fully
iterative approach to the forearc geotherm), and at this
distance (~100 km) inboard of the final trench interface, there is
limited scope for further rollback after emplacement of the nappe of interest.

The potential for disequilibrium processes such
as slab window heating to disrupt the geotherm at depth during the long
residence time beneath the crust are not considered in the model. <!--
(This is confusing, I thought that was one of our scenarios. This needs
to be clarified) -->
There are no reliable estimates of the mantle heat flux that cover the model
domain, and the thermal environment for underplated mantle lithosphere is complicated
by the presence of a subducting slab below the model domain at some depth. The model
is run to great depth to avoid any influence on the surface geotherm. However,
Farallon and forearc scenarios can be treated as maximum temperatures because of
the influence of the overriding slab. <!-- (not sure what you are
talking about here. What is “forearc scenarios”) -->

<!--[[model_results]]-->


### Model results

Model results are presented in \figref{model_results} and
\figref{model_comparison}.
For the underplating scenarios, <!-- why plural -->the @Royden1993a forearc model
predicts low temperatures (~235-245 ºC) at the subduction
interface. This is quite low relative to the temperatures predicted for
the Sierra Pelona schist (~700 ºC) by @Kidder2013, or
700-800 ºC derived as an emplacement constraint for the Sierra de
Salinas schist [@Kidder2006]. In the stalled
Monterey-plate scenario, temperature is predicted to be
980 ºC at the subduction interface. Despite this uncertainty in subduction conditions, the
model is much more sensitive to the thermal history of the oceanic plate
than to the forearc geotherm. For all longer run-time models (both the
forearc <!-- ??? --> and Farallon scenarios), this may prove to be a major factor.

The baseline scenario with late Cretaceous rollback and temperatures
pinned to the Sierra de Salinas schist has a very similar final thermal
structure to the older stalled slab scenarios <!-- do we show these in
the model? -->, showing that the
high subduction-channel temperatures experienced during late-Cretaceous flat slab
subduction and schist metamorphism do not have a long-lasting impact on the
thermal structure of the margin. Thus, these cannot be
explain the elevated temperatures experienced by the Crystal Knob
peridotites.

The model predicts much higher temperatures <!-- (do you mean to say a
much higher thermal gradient, or surface heat flow, or both, or if not
much higher temperatures where, and relative to what?) --> for the slab window than
for the Farallon-plate or stalled-slab models, which corresponds to
previous studies @Erkan2008. However, these studies concluded that the
effect must be due to a stalled slab, where in fact underplated Farallon mantle nappes satisfy the surface heat flow data equally well.


It is possible that the slab could be older.
But, thermal relaxation of an old slab would not contribute any heat to explain
elevated heat flow values in Coast Ranges (CRTA).
<!-- What is CRTA? Maybe you should email me Erkan and Blackwell. Are
these, or is this, several points, or a single point of high heat flow
measurements within the regional field of low heat flow measurements. If
so where are these point(s). They could be important in terms of deep
heat advection, in terms of why a 1.7 Ma lava would erupt in the region)
-->

@Erkan2008 pointed out that heat flow for the stalled slab scenario was too low to
fully explain anomalous heat flows in the Coast ranges.
Model-predicted heat flows lower than measured values could be explained
by added heat flux from shear heating [@Thatcher1998] or erosion [@Mancktelow1997;@England1990]

<!--[[model_comparison]]-->

Estimating erosion is beyond the scope of this study, but pulses of recent erosion
in the Coast Ranges are <!-- see Ducea et al. (2003) for rapid late
Cenozoic uplift of the Santa Lucia’s -->

- Correspond to results of @Erkan2008
