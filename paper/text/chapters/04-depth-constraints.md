## Depth constraints

<!--[[depth]]-->

Pyroxene-exchange geothermometry shows that the peridotite samples form
two groups in temperature with centroids separated by roughly 60ºC.
This temperature range likely corresponds to an array of sample sources
along a depth gradient.
The depth of the xenolith samples in the mantle lithosphere, coupled
with equilibration temperatures, provides a fully-defined constraint on the
geotherm beneath Crystal Knob at the time of eruption. For spinel
peridotites, equilibration depths can only be analytically
estimated within broad boundaries. With no reliable geobarometers for spinel peridotites,
several less robust metrics are used to evaluate the depth
of the xenolith source. We present several lines of reasoning suggesting that the
xenoliths were sourced along a depth gradient relatively deep within the spinel stability
field, between roughly 45 and 75 km.

Several of the techniques below produce estimates of pressure, rather
than depth. To discuss these data in depth--temperature space, we correct
them using a hydrostatic gradient of ~0.03 GPa per km across the mantle lithosphere,
based on integration of the crustal and mantle densities given in @tbl:model_parameters.

<!--[[ree_temperatures]]-->

### Limits of spinel stability

Entrainment depths of all peridotite xenoliths must be greater than ~30 km,
the depth of the Moho near the Crystal Knob eruption site [@Trehu1991],
which will be discussed in more detail in @sec:tectonic_scenarios.
Another minimum depth constraint is the plagioclase--spinel peridotite
facies transition, which occurs at depths of 20-30 km but is
highly composition-dependent [@Green1970a; @Borghini2009], with high-Cr
harzburgites stable to the surface.

The high-pressure boundary of spinel stability limits maximum possible
entrainment depths.
The spinel--garnet peridotite facies transition is
composition-dependent and poorly constrained for
natural systems, but thought to lie over the 50-80 km depth interval
[@ONeill1981; @Kinzler1997; @Gasparik2000; @Klemme2004].
The breakdown depth of spinel is strongly dependent on temperature and composition, particularly
the amount of refractory Cr hosted by spinel.
Several experimental and thermodynamic studies have attempted to
estimate the magnitude of this effect.
@ONeill1981 presented experiments both with and without Cr and described
a simple empirical relationship of spinel-out depth with Cr content and temperature.
@Robinson1998 suggests that, given fertile "pyrolite" compositions with little
Cr, garnet is unstable at depths less than 80 km at the peridotite solidus (~1470ºC at this depth).
Subsolidus experimental results show that the maximum depth of the spinel
stability field in the absence of Cr ranges from 1.8-2.0 GPa (55-60 km) at 1000-1200ºC
[@Klemme2000].
Chromian spinels can be stable to much greater depth:
thermodynamic modeling by @Klemme2004 suggests a broad garnet-spinel
co-stability field (up to a spinel-out reaction at 5 GPa for Cr# of ~30),
but a spinel-weighted metastable assemblage is possible even
at higher pressures.

As shown in @fig:major_elements|c, samples in the high-temperature cohort (CK-3, CK-4, and CK-6) have
higher spinel Cr# than the low-temperature samples. This enrichment in
refractory Cr arises from the increased depletion of these samples and
expands the stability field of spinel against garnet to deeper depths.

Though @Robinson1998, @Klemme2000, and @Klemme2004 show a high-pressure
phase transition with a complex compositional dependence,
the rough estimate of the garnet-in pressure
given by @ONeill1981 performs sufficiently well at T < 1200 ºC.
This empirical relationship is used in @fig:depth to graphically illustrate
the phase-transition depths given the Cr# of each sample (with error
bars of 0.15 GPa).

This simple treatment provides a high-pressure constraint on the Crystal Knob
xenolith source. The
maximum possible entrainment depths of the high-Cr samples increase by
up to 15 km relative to Cr-free compositions, from ~65 km for the
low-temperature samples to maximum depths of ~80 km for the high-temperature cohort.

### Ca-in-olivine barometer

Equilibration pressure measurements are attempted for the peridotite
xenoliths using the @Kohler1990 Ca-in-olivine
barometer, which is based on the decreasing abundance of Ca
in olivine with pressure. This barometer is explicitly calibrated for spinel
peridotites but should be treated with caution based on poor resolution,
high temperature dependence,vulnerability to late-stage diffusion, and dependence on low Ca
concentrations in olivine near analytical thresholds for
electron microprobe analysis [@Medaris1999; @OReilly1997].

To model the variability of model pressures due to analytical uncertainties,
barometry is applied separately for nearest-neighbor pyroxene and olivine measurements.
Analytical errors are propagated through the calculation.
To correct for the mild pressure dependence of the two-pyroxene thermometer, and the
temperature dependence of the olivine barometer, we jointly solve temperature and
pressure by iteratively optimizing to a common solution for each set of
microprobe measurements.
This yields a set of separate internally consistent depth and temperature
measurements for each sample corresponding to individual pairs of
microprobe measurements.
In @fig:depth, we show the full pressure--temperature error space for each
sample by applying a Monte Carlo random sampling ($n=100,000$) to the analytical
errors on each pressure estimate.

The Ca-in-olivine barometer yields a broad distribution in model depths,
largely coincident with the spinel stability field [@fig:depth]. The depth
distributions are largely normal, with modes ranging from 40 to 53 km. Within
the Crystal Knob sample set, the low and high-temperature cohorts remain
separable, with high-temperature samples showing deeper equilibrium depths. The
scale of the errors within a single sample reflects the barometer's strong
covariance with major-element thermometers, as well as its sensitivity to small
variations in Ca concentrations. The bulk of the spread in the data reflects
the poor calibration of the barometer itself. The low-temperature samples in
particular have significant scatter towards depths above the spinel-in isograd.
The small Ca cation diffuses rapidly during transient heating [@Kohler1990],
which produces a shallowing bias on the depth distribution.
This may explain why CK-4, the most altered sample, has a depth mode
~10 km shallower than the other samples (CK-3 and CK-6) with similar equilibration temperatures.
The temperatures derived from the independent REE system are higher
than the major-element temperatures for several samples in the high-temperature
cohort (CK-4 and CK-6), which may point to these samples being derived from a greater
depth within the distribution of Ca-in-olivine depths.

Despite the imprecision of the method, Ca-in-olivine barometry
suggests that the samples were sourced from relatively
deep within the spinel stability field, at
depths of ~40 km or greater. This preference is amplified by
comparisons with depth estimates of the thermal state of the mantle
lithosphere derived from regional heat flow datasets.

### Comparisons with steady-state heat flow

The depth constraints derived from xenolith thermobarometry above
can be compared to surface heat-flow and seismic
constraints on the regional geotherm.

Given our high-confidence temperature measurements for the Crystal
Knob xenolith suite, we can generate model entrainment depths
by pinning the samples to a conductive geotherm constrained by surface heat flux.
These can be useful for comparisons with our intrinsic depth constraints from
thermobarometry.
In @fig:depth, we show potential steady-state geotherms for surface heat fluxes
ranging from 60 to 120 mW/m^2, all of which intersect the potential
depth distributions from spinel stability and Ca-in-olivine barometry.

These geothermal gradients are calculated using thermal conductivity and
diffusivity given in @tbl:model_parameters for the crust to a depth of
30 km, and mantle lithosphere below this level.
No fixed amount of radiogenic heat production is assumed, but the average empirical
factor of 0.6 proposed by @Pollack1977 is used to
reduce surface heat flux to a presumed mantle contribution, with
the remainder being taken up by radiogenic heat production near the surface.
We use a radiogenic contribution that exponentially decreases with depth
with a characteristic length scale of 10 km.
The amount of heat emanating from the mantle and the presumed thermal conductivity
across the lithosphere are the main
controls on the slope of the modeled geothermal
gradient. This methodology is developed in @Turcotte2002 and is
identical to that used by @Luffi2009, except that crustal
thermal conductivity is reduced to match our conditions for dynamic
thermal modeling [@sec:modeling]. This yields a slightly "hotter"
geotherm throughout the mantle lithosphere.

Phase stability constraints on the Crystal Knob xenoliths correspond to a broad
range of plausible lithospheric conductive geotherms.
The hottest potential geotherm keeping the sample set within the spinel stability
field is > 120 mW/m^2 at the surface.
Accounting for the Cr-dependent
depth of the spinel--garnet transition, the 65 mW/m^2 conductive geotherm is
the coolest that places all samples within the spinel stability field.
The centroids of the Ca-in-olivine model depth distributions broadly
correspond to surface heat flows ranging from ~70 to 110 mW/m^2.

Using a database of surface heat flows for North America,
@Erkan2009 estimate regionally-averaged heat flows of 80-90 mW/m^2 for the
central California coast, including the vicinity of Crystal Knob.
Projection of the TA98 temperature distribution onto our calculated
steady-state geotherms yields model depths of ~45-55 km for the
Crystal Knob sample set. This depth range falls within the spinel stability field
and near the center of the depth distributions extracted using
Ca-in-olivine barometry. However, depths derived from surface heat flows
may be underestimates, for reasons discussed in @sec:heat-flow.

### Summary of depth constraints

The integration of depth constraints on the xenolith samples from multiple
techniques gives a broad boundaries on the depth of origin of the Crystal
Knob xenoliths within the mantle lithosphere at the time of their eruption. For
reasonable slopes of the sub-Salinian geotherm, the range of temperatures in
the sample set indicates sourcing over a depth range of 5-10 km within the
mantle lithosphere. These depths must be greater than 30 km, the depth to the
Moho, and less than 60-90 km based on the composition-dependent lower limit of
the spinel stability field. Ca-in-olivine barometry suggests a tighter set of
constraints near the center of the spinel stability field. Model depths of
45-55 km prepared from steady-state geotherms agree with this assessment, but
might be underestimates. Given the bias in both Ca-in-olivine and heat-flow
measurements towards shallower depths, we take the depth range of 45-75 km as
a likely entrainment depth for the Crystal Knob xenoliths.

This assessment of relatively deep entrainment of the Crystal Knob xenoliths
along a fairly "cool" geotherm conforms to constraints from independent
studies. Estimates of the thermal state of the deep lithosphere derived from
seismic tomography show temperatures of 700--1100ºC occurring at depths of
50--100 km for coastal California [@Goes2002], corresponding to cooler
geotherms than predicted by surface heat flow. More recent estimates put the
depth of the lithosphere-asthenosphere boundary at roughly 70 km in the
southern Coast Ranges [@Li2007]. Given estimates that the subcontinental
lithosphere-asthenosphere boundary occurs at 1200-1300ºC
[e.g. @OReilly2010; @Fischer2010], this corresponds to steady-state
geotherms of 70-80 mW/m^2.

We next turn to the accuracy of this extrapolation from heat flow values,
and its implication for understanding the thermal structure of the lithosphere.

