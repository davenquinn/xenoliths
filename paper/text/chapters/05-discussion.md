
Discussion
==========

## Petrology

The peridotite samples from Crystal Knob show a range of depletion in
major and trace elements. They are isotopically depleted, with an
$\epsilon_\mathrm{Nd}$ of
+10, and \ce{^{87}Sr}/\ce{^{86}Sr} of .7029. <!-- (Daven, the Nd and Sr
data in Table 4 are given as measured. In the table you should also show
the time corrected Nd and Sr isotopic ratios and epslon Nd  value for a
correction of 1.65 Ma. You should then refer to these time corrected
numbers in the text and show these values on the Figure 10 Eps Nd-Sr
plot. The corrections will be small, but since we have dated the host it
would be best to use the time corrected values for time of entrainment.
--> This corresponds to the depleted asthenosphere, or convecting upper mantle of Hoffman (2004), with a
mantle upwelling source that has seen no contribution from the western
North American crust or continental lithosphere more generally.

Pyroxene-exchange geothermometry shows that the peridotite samples form
two groups in temperature with centroids separated by roughly 60ºC.
These temperatures seem to correspond to the samples being sourced along
a depth gradient. For reasonable slopes of the sub-Salinian geotherm,
this range of temperatures may sample a depth range of 5-15 km within
the mantle lithosphere. These depths must be greater than 30 km, the
depth to the Moho, <!-- appropriate reference --> and less than
60-90 km based on the composition-dependent lower limit of the spinel stability field.

### Rare-earth temperature

Rare-earth exchange thermometry shows the same two groupings of
temperatures. Temperatures measured for the low-temperature cohort are
most comparable to the TA98 results. Given that the TA98 method has been
found to perform best among the pyroxene-exchange thermometers by
@Nimis2010, it seems likely that both the TA98 and REE temperatures show
long-term equilibrium with no significant thermal perturbations. For the
high-temperature cohort, particularly samples CK-4 and CK-6, the REE
method shows significantly higher equilibration temperatures than the
TA98 method. Rare-earths in pyroxene diffuse several orders of magnitude
slower than major elements [@Liang2013], so early thermal events can
leave an imprint on the distribution of rare-earths for much longer than
with major elements. It is likely that these higher temperatures are a
signature of a fossil heating event primarily affecting the deepest
samples. This is accompanied by major REE disequilibrium in sample CK-4,
which also contains the most intergranular melt channels.

Sample CK-4 records a significantly higher temperature for LREE than the
other samples and its HREE equilibration temperatures. This signifies
that LREEs were equilibrated at a much higher temperature than the
HREEs. This pronounced within-sample disequilibrium could be the result
of metasomatic processes, which is bolstered by the fact that CK-4 has
the only significant melt-infiltration textures in the sample set. It is
likely, therefore, that CK-4 was subjected to a short, transient heating
event that was not fully equilibrated in HREE. Further, since this
transient heating is not reflected in major-element temperatures, it is
likely that the sample was heated transiently and equilibrated at a
lower temperature for a significant period of time. Also, given low CPX modes,
rare-earths added during refertilization may not be completely
homogenized throughout the sample.

### Trace elements

For clinopyroxenes, the low-temperature cohort ranges from essentially
undepleted (CK-7 has a flat chondrite-normalized REE profile) to low
levels of depletion characteristic of the least-depleted abyssal
peridotites \figp{cpx_literature_comparison}. The high-temperature
cohort seems to have been both depleted (based on low HREE
concentrations) and re-enriched in trace elements to a much greater
degree than the low-temperature samples.

<!-- (Daven, do you think that the high-T group attained its signature
at the Farallon-Pacific spreading ridge, or from re-heating of
underplated Farallon mantle by the slab window convection event?). -->


In whole-rock space, the relationship between sample temperature and level of
depletion is less clear.
Combining pyroxene trace-element measurements with modal mineralogy
suggests that pyroxene modes have changed significantly in response to
depletion, making recalculated whole-rock trace elements a valuable tool
to assess the overall level of depletion in the sample.
Sample CK-5 in particular is much more depleted in whole-rock
composition than its cpx trace-element composition would suggest, due to
low clinopyroxene modes.

### Modeling depletion and re-enrichment

A depletion model is constructed
in *alphaMELTS* [@Smith2005b] to illuminate the probable depletion and
re-enrichment paths of the Crystal Knob sample.
A generic model of peridotite depletion is constructed, in which
a parcel of material starting at a mantle
potential temperature of 1470ºC at 3.0 GPa
and a depleted MORB mantle composition [@Workman2005] is
tracked along an isentropic fractional melting path with a melt porosity of 1%.
These starting parameters were chosen to provide the best correspondence
with the overall experimental dataset.

The HREE (Er--Lu) composition of Crystal Knob xenolith samples are fit
to model step along this adiabatic path using least-squares error
minimization.
Since HREEs are not likely to be
easily modified by late re-enrichment due to their low diffusion rates,
the best-fitting model step is used as an estimate of single-stage
depletion of the samples during decompression melting. 

The difference between the sample composition and this fitted depleted
profile is taken as the contribution from batch addition of an
enriching fluid. The REE concentrations of the enriching agent are then
normalized to an average of 12$\times$primitive mantle.
The normalization factor employed to shift the composition of enriching
fluids to this value is shown in Figure \ref{fig:ree_trends} and corresponds
roughly to the amount of LREE added during re-enrichment.

The results of this model show that
the samples are variably depleted and all except CK-2 are re-enriched to
some extent \figp{ree_model}. CK-2 appears to be in equilibrium with mid-ocean ridge
basalt while the others appear to be in equilibrium with an enriching
agent similar to alkali basalt. The strong exponential increase in the
presumed LREE composition of our enriching material shows that the
re-enrichment is likely better modeled as a fractional process. Variable
amounts of interaction with the enriched fluid are required to explain
the observed level of re-enrichment, with the most seen by samples CK-3
and CK-4 \figp{ree_trends}.

Primary depletion degrees of the xenolith samples are estimated by finding
the model compositions which best fit the whole-rock HREE, MgO, and
\ce{Al2O3} composition of each sample. Results are summarized
in Table \ref{tab:depletion degrees} and are superficially similar to
the trends visible in modal abundance \figp{modes} and trace element
\figp{spider} data. The degree of depletion generally increases
with the modeled temperature of the sample, with the notable exception of
sample CK-6, which is by far the least-depleted sample by major-element
proxies and only moderately depleted in heavy rare-earth elements,
although it has the hottest modeled temperature.

Sample CK-6, although relatively fertile,
has much higher iron than the other samples. This makes
it seem likely that it was re-enriched from a more evolved source than
the baseline primitive mantle.

<!--[[ree_model]]-->
<!--[[ree_trends]]-->

<!--[[depletion_degrees]]-->

The overall pattern of trace elements suggests that the xenolith samples are residues of progressive
fractional melting of primitive mantle to form abyssal peridotites [@Johnson1990].
The samples underwent
a multistage history of wholesale REE depletion (due to higher-degree
melting) followed by later LREE re-enrichment by an enriched fluid.
This overprint is similar
to that gained by emplacement at a mid-ocean ridge followed by
refertilization by off-axis magmatism [@Luffi2009]. However, it may also
have arisen during melt extraction and entrainment prior to eruption.
The latter seems to demand a significant residence time of the hotter
xenoliths in a magma chamber at depth to allow LREE refertilization.

### Host lava

Extension in the lower crust?
Of family with small eruptive episodes such as Coyote Creek (based on
eruptive age)

Fossil heating event affecting CK-4 LREE. This is not the most recent perturbation because it's not reflected in the major element thermometers

## Origin of mantle lithosphere beneath the Crystal Knob volcanic neck

Rb-Sr and Sm-Nd isotopic data on peridotite xenoliths from this study
demonstrate that the mantle lithosphere that was sampled by the Crystal
Knob volcanic neck is sourced from the depleted convecting mantle with
no contribution from recycled crustal material, nor ancient
sub-continental mantle lithosphere. This is consistent with the neck
having penetrated through the Franciscan accretionary complex, and also
with the observations that Salinia continental arc rocks of the region
are unrooted nappes that lie structurally above Franciscan complex
rocks. In that the Franciscan complex of the region was assembled by
long-lived subduction of the Farallon plate encompassing
Cretaceous-early Tertiary time [@Cowan1978; @Saleeby1986; @Seton2012; @Chapman2016a],
it follows that the mantle lithosphere of the region was constructed from partly subducted Farallon
plate upper mantle at some point late in the Franciscan accretionary
history, or by some other mechanism following the cessation of Farallon
plate subduction. The geologic history of the region integrated with
crustal structure constraints pose viable alternatives for these
mechanisms.

## Late Cenozoic tectonic history and regional crustal structure

In Oligocene to early Miocene time the Pacific-Farallon spreading ridge
obliquely impinged into the SW Cordillera subduction zone leading to the
development of the San Andreas transform system [@Atwater1970]. Ridge
impingement was kinematically complex due to large offset ridge-ridge
transforms, resulting in the opening of a geometrically complex slab
window as well as the production of the Monterey microplate, which
nucleated as an oblique intra-oceanic rift along an ~250 km long segment
of the Pacific-Farallon ridge [@Thorkelson1989; @Bohannon1995; @Atwater1998; @Wilson2005].
Late Cenozoic volcanism of the coastal region of central California has been
linked to slab window formation by the partial melting of asthenosphere
as it ascended into the slab window [@Wilson2005].
Alternatively, it has been suggested that microplate formation along the
impinging Pacific-Farallon ridge was more dominant than slab window
formation, and that these microplates stalled beneath coastal central
California as the Farallon plate continued to subduct deeper into the
mantle [@Bohannon1995; @Brocher1999; @VanWijk2001]. Late Cenozoic
volcanism of the region, in this scenario, is linked to the
youthfulness of the subducted microplate(s), implying an
“upside down” partial melting mechanism within and immediately adjacent
to the lithospheric lid. Both the slab window (or gap) and stalled
microplate hypotheses are based on plate kinematic relationships, which
upon closer analysis appears to require a combination of both slab
window and stalled oceanic microplate segments
[@Bohannon1995; @Atwater1998; @tenBrink1999; @Wilson2005].
Seismic data cited in support of the stalled slab hypothesis consist of
an 8-15 km thick low east-dipping mafic lower crustal layer that extends
beneath central California from the offshore region into proximity of
the San Andreas fault, and which thickens eastwards over Moho depths of
\~12-30 km [@Brocher1999]. Strong internal reflectivity within this layer
[@Trehu1987; @Brocher1999], and sharp
inflections in its upper surface [@Trehu1991] indicate that this mafic
layer is internally deformed and imbricated, which accounts for its
thickness exceeding typical oceanic mafic crust by a factor of two to
three.
<!-- Also see @Fuis1998, a review of Coast Range structure along the margin -->
Such imbrication and underplating require a basal detachment,
which most logically is the underlying Moho. In this context the
regions’s lower crustal mafic layer is more plausibly interpreted as a
regional underplated duplex of Farallon plate oceanic crustal nappes
that accreted during Franciscan subduction. The underlying mantle
lithosphere could be underplated Farallon plate mantle, and/or Monterey
microplate mantle with its crustal section left imbricated along the toe
of the mafic duplex in the offshore region. The Crystal Knob xenolith
suite is the only known direct sampling of this underplated mantle.

The pre-Neogene tectonic setting of the Crystal Knob eruption site is
shown in Figure 18 by restoration of the San Andreas dextral transform
system [@Matthews1976; @Dickinson2005; @Chapman2012; @Hall2013; @Sharman2013].
The Crystal Knob eruption site restores to a position outboard of the southern California
batholith. The principal windows into shallowly underplated subduction
channel schists are shown on Figure 18 along with the principal upper
plate batholithic exposures. The intervening areas left white denote
latest Cretaceous-Cenozoic overlap strata. On Figure 18 the current
western extent of the Salinia crystalline nappes is shown as the
Nacimiento fault and the offshore Farallon escarpment. Crystalline rocks
of the Salinia nappes extended westwards across Nacimiento belt
Franciscan an unknown distance [@Hall2013], but have been
eroded off their lower plate complex as the coastal region has risen in
the Pliocene [@Ducea2003].

The Figure 18 reconstruction exhibits the first-order crustal relations
that pose three highly plausible origins for the sub-Crystal Knob mantle
lithosphere: 1. shallowly ascended asthenosphere within the
Pacific-Farallon slab window [@Atwater1998]; 2. subduction
underplated, or stalled Monterey oceanic microplate [@Bohannon1995];
or 3. underplated Farallon plate mantle lithosphere nappe(s) that lie in structural sequence with the upper mantle duplex
resolved beneath the Dish Hill xenolith location [@Luffi2009].

## Slab windows and Monterey plate

Figure 18 shows the surface projection of the hypothetical slab window
and the partially subducted Monterey plate at ca. 19 Ma [@Wilson2005].
The slab window is thought to have formed by the subduction of the trailing edge of the Farallon plate, unsupported by sea floor
spreading along the former spreading axis with the Pacific plate. The
Monterey plate nucleated along an ~250 km long segment of the
Pacific-Farallon ridge as an oblique rift that was rotated ~25º clockwise
from the Pacific-Farallon rift axis [@Atwater1989].
It’s generation was synchronous with the early stages of
Pacific-Farallon plate convergence into the Cordilleran subduction zone
along the southern California coastal region, and coincided with
transrotational rifting of the continental borderland region and
displacement of the western Transverse Ranges bedrock
[@Bohannon1995; @Atwater1998]. The current position of the Monterey plate,
relative to the Crystal Knob eruption site, is a result
of dextral displacements linked to borderland transrotational rifting,
subsequent ~155 km-scale dextral offsets along the San Gregorio-Hosgri
fault system, and possible additional dextral offsets in the offshore
region (Fig. 3). A number of workers have suggested that translation of
the Monterey plate along the San Andreas system entailed significant
sub-horizontal fault segments that accommodated dextral displacements
[@Furlong1989; @Pikser2012]. As of yet, however, all
remotely imaged segments of the transform system have been shown to be
steeply oriented [@Dietz1990; @Brocher1999; @Yan2005; @Titus2007; @Yan2007; @Ozacar2009].
According to the Figure 18 reconstruction the Crystal Knob eruption site
was above the Pacific-Farallon slab window ~50-100 km north of the
northeast margin of the partially subducted Monterey plate. The narrow
slab window segment shown along the eastern edge of the partially
subducted plate marks the plate’s separation locus with the Farallon
plate, which subsequently opened wider beneath the southern California
region as the Farallon plate descended deeper into the mantle
[@Atwater1998; @Wilson2005]. Over the time interval of ca. 22-10 Ma the Monterey plate’s dextral motion relative to the subducting
trench had a nontrivial divergence component, as a result of it’s
coupling to the Pacific plate. The likelihood of extensional attenuation
of the underthrust portion of the Monterey plate during such divergent
motion is non-explored, but strongly implied in \citet[]['s]{Bohannon1995} reconstruction.
Coupling of Monterey plate divergent motion
across the subduction megathrust break is hypothesized to have driven
dextral transrotational rifting [@Bohannon1995]. As western
Transverse Range rock panels rotated into their current position from
transrotational rifting, the Monterey plate continued its northward
displacement along the San Gregorio-Hosgri fault system (Fig. 3). Note
that on Figure 18 the outer edge of the Farallon-Monterey slab window is
on trend with the San Gregorio-Hosgri fault system. Distinct steps and
inflections in lower crustal velocity structure across this fault system
[@Brocher1999] indicates that it cuts the entire crust. This
poses the likely possibility that the San Gregorio-Hosgri fault system
bounds the eastern margin of underplated Monterey plate in the coastal
central California region. This is in line with seismic observations
showing an ~16 E dip to the Monterey plate offshore, with a typical
abyssal crustal thickness, juxtaposed against a nearly flat thickened
lower crustal layer beneath the Nacimiento Franciscan  [@Trehu1991; @Nicholson1992].
These observations are in direct conflict with the notion that a structurally continuous mafic layer constitutes the
lower crust beneath the central coastal California and adjacent offshore
region, as dismissed in the discussions above.

The analysis presented above argues against models of the Monterey plate
having been translated horizontally as a “dangling slab” through the
upper mantle of the coastal region of southern to central California by
its coupling to Pacific plate motions [@VanWijk2001; @Pikser2012; @Wang2013].
This can be argued against on the basis of seismological, geodynamic and surface geological relations.
All such models rely on the untenable notion that a structurally continuous mafic
layer, representing stalled Monterey plate, constitutes the lower crust
beneath the entire coastal central California and offshore region (see
above). These studies further suggest that the Monterey “dangling slab”
currently corresponds to the high-wave speed anomaly of the southern
Sierra Nevada-Great Valley region (Fig. 1), commonly called the
“Isabella anomaly”. However, seismological and geodynamic studies much
more rigorously show that this anomaly represents the convectively
mobilized mantle wedge, or mantle lithosphere, derived from beneath the
eastern and southern Sierra Nevada batholith
[@Zandt2004; @Frassetto2011; @Gilbert2012; @Saleeby2012; @Jones2014; @Levandowski2015].
In addition to the structural continuity that these studies show between the seismic
anomaly and the residual mantle lithosphere that is still in place
beneath the Great Valley and Sierra Nevada (Fig. 3), these studies show
that the volume of the Isabella anomaly far exceeds a reasonable volume
estimate for the attenuated terminus of a hypothetical translated
Monterey slab. These studies also provide mechanisms for lower crustal
plastic deformation, observable surface faulting, upper mantle–lower
crustal partial melting and dynamic topographic effects that are ignored
in the dangling slab hypothesis. Surface geological effects of such
melting and topographic transients are closely correlated to the
convective mobilization of the sub-Sierran mantle lithosphere
[@Ducea1998b; @Farmer2002; @Saleeby2013; @Cecil2014; @Levandowski2015].
The surface effects of Monterey plate partial subduction followed by transtensional coupling to Pacific
plate motions are closely correlated to transrotational rifting in the
southern California Borderland and the linked clockwise rotation of
western Transverse Ranges bedrock panels [Fig. 3; @Bohannon1995; @Wilson2005].
This is in line with the Monterey slab’s limited down-dip extent as bounded by the Monterey-Farallon slab window
segment shown on Figure 18. If the hypothetical Monterey “dangling slab”
were of proper proportion to form the Isabella anomaly, then why were
its effects on surface geology restricted to the Borderland and
Transverse Ranges? Epeirogenic transients that correlate to the
convective mobilization of the sub-Sierran mantle lithosphere as the
Isabella anomaly are highly out of phase with the predicted translation
pattern for a “dangling” Monterey slab [@Saleeby2013; @Cecil2014].
Possible remnants of necked off partially subducted Monterey plate are more plausibly correlated to the Transverse Ranges high-wave
speed anomaly in terms of position and volume (Fig. 3), and also have a
firm geodynamic basis as such [@Burkett2009].

According to the @Wilson2005 reconstruction of the
Pacific-Farallon slab window and adjacent Monterey plate (Fig. 18), the
Crystal Knob eruption site was located above a slab window in the early
Neogene, proximal to the northeastern boundary transform edge of the
Monterey plate. Diffuse volcanism, some clearly derived from
decompression partial melting of convecting mantle, is widespread for
this time period across the region of the reconstructed slab window
[@Hurst1982; @Sharma1991; @Cole1995; @Wilson2005].
However, this phase of slab window opening and related volcanism
cannot account for the eruption of the ca. 1.7 Ma Crystal Knob volcanic
neck, which we return to below.

## Underplated Farallon Plate mantle nappes

The reconstruction of the Crystal Knob eruption site to its pre-San
Andreas position (Fig. 18) poses a highly viable alternative for the
development of the site’s underlying mantle lithosphere. This is
particularly viable in light of the neck having erupted through the
Nacimiento belt of the Franciscan complex, immediately adjacent to the
current outer limit of Salinia crystalline nappes (Fig. 1).  Accretion
of the Nacimiento belt occurred in the Late Cretaceous beneath the outer
reaches of the Salinia nappe sequence [@Hall2013; @Chapman2016a].
In their core area the Salinia nappes rode westwards on slightly older, higher metamorphic grade, Franciscan rocks that are
shown on Figures 1 and 18 as windows into subduction channel schists
[@Barth2003; @Kidder2006; @Ducea2009]. As
discussed earlier, the southernmost Sierra Nevada-western Mojave
“autochthon” for the Salinia nappes is likewise detached from its
original mantle wedge underpinnings, and shingled into crystalline
nappes that lie on underplated high-grade subduction channel schists as
well [@Saleeby2003; @Chapman2010; @Chapman2012; @Chapman2016b]. Tectonic
erosion of the mantle wedge followed by shallow subduction underplating
of Franciscan rocks requires subsequent reconstruction of the current
mantle lithosphere. As discussed above, @Luffi2009 present
findings on the Dish Hill and Cima mantle xenolith sites (Fig. 1) that
suggest the presence of a mantle lithosphere duplex with multiple
Farallon plate upper mantle nappes in structural sequence beneath a
residual roof of continental mantle lithosphere. In that the crustal
structural sequence of the western Mojave region correlates closely to
that of the Salinia nappes, spatially and temporally [@Chapman2010; @Chapman2012],
it stands to reason that upper mantle duplex accretion progressed
westwards from the Mojave region to beneath the Salinia
nappes as well as the Nacimiento belt of the Franciscan.

In Figure \ref{fig:cross_sections} we present a model for Farallon plate mantle lithosphere
having tectonically underplated the Mojave-Salinia-Nacimiento segment of
the SW Cordilleran convergent margin in the Late Cretaceous [after @Saleeby2003; @Luffi2009].
This is shown to have occurred in conjunction with shallow flat subduction of the Shatsky Rise conjugate
LIP [after @Saleeby2003; @Liu2010]. The approximate age of
Farallon plate entering the trench is shown on each frame [after @Seton2012].
Crustal deformation, timing and thermal conditions, as
applied to our thermal modeling presented below, are integrated from
@Kidder2006 and @Chapman2010; @Chapman2012; @Chapman2016a. Figure
17a and b show the arrival of the oceanic plateau into the subducting
trench, and plateau buoyancy driven shallowing of the subduction
megathrust, which drove tectonic erosion of the mantle wedge.
Temperature conditions along the flat subduction megathrust initiated at
\~900ºC, ambient conditions within the deep levels of the then-active
arc, and retrogressed to ~715ºC, peak temperatures recorded in shallowly
subducted metaclastic rocks of the Sierra de Salinas schist, exposed in
the principal Salinia window into the subduction channel schists [@Kidder2006].

In Figure \ref{fig:cross_sections}C and D we adopt the focused slab rollback and mantle
lithosphere underplating models of @Saleeby2003 and @Luffi2009,
for the dynamic response of normal thickness oceanic lithosphere
following the crustal thickened oceanic plateau down the subduction
zone. Principal crustal responses are shown as large magnitude
trench-directed extension coupled to regional extrusion of the
underplated subduction channel schists, which was driven by suction
forces of the retreating slab. In the Figure \ref{fig:cross_sections}c to d transition,
accelerated rollback is accomplished by duplex formation from Farallon
plate mantle nappes. We suspect that mantle nappe detachment was
controlled primarily by the temperature control on the brittle-plastic
transition in olivine. For ca. 40-50 m.y. old oceanic lithosphere
entering the subduction zone (Figures \ref{fig:cross_sections}c and d),
an estimated ~700-800 ºC
control on this transition [@Warren2006; @Burgmann2008; @Mei2010] occurs
at ~25-40 km depth in the slab [@Doin1996]. We also suspect that the retreat of the slab as it
subducted imparted a significant tensile stress component within the
slab that was oriented at high angle to the subduction megathrust, which
further promoted nappe detachment. The nucleation of detachment surfaces
was likely controlled by hydration fronts that followed primary normal
and transform faults within the upper oceanic lithosphere. The lack of
high-pressure mafic schist samples in both the Crystal Knob and Dish
Hill xenolith suites suggests that oceanic crust was detached during
mantle nappe detachment, presumably at oceanic Moho depths, to be
underplated as the seismically imaged thickened mafic lower crust of the
region [@Trehu1991; @Brocher1999]. On the basis of the regional
structural evolution of the central to southern California basement, and
on the petrogenetic history recorded in the region's mantle xenolith
suites, we consider the Figure \ref{fig:cross_sections}d section to be that most likely sampled by
the Crystal Knob eruption. This section is idealized for Late Cretaceous
time, and below we layer on the complexity of late Cenozoic faulting in
our analysis. We focus now to thermal history in order to more
thoroughly pursue the possible origins of the sub-Crystal Knob mantle
lithosphere.

## Thermal considerations

Regardless of the generalized lithospheric structure depicted in Figure
17, kinematic reconstructions of the impingement of the Pacific-Farallon
spreading center with the SW Cordilleran subducting trench require a
slab window beneath the Crystal Knob eruption site in the early Neogene
[@Atwater1998; @Wilson2005]. The depth of
asthenospheric underplating related to slab window opening is poorly
constrained, and likely to vary geographically as a function of
thickness and thermal variations in the pre-existing lithospheric lid,
as well its state of stress and structural coherency. Though volcanism
in the central California Coast Ranges has been tied to slab window
opening, its volume has not been consistent with volcanism associated other episodes of
shallow asthenospheric upwelling in the Cordillera particularly in the
forearc region of coastal central California [@Humphreys1995] <!-- not
familiar with this ref, please double check for its applicability-->.
This is readily explained if the slab window opened beneath a tiered
duplex of underplated Farallon mantle nappes, roofed by a duplex of
underplated Farallon oceanic crust (lower crustal mafic layer), in turn
roofed by the Nacimiento Franciscan and Salinia nappes. Our estimate of
a 50-80 km depth interval over which the Crystal Knob lavas sampled the
underlying mantle lithosphere (Fig. 14), coupled with a general lack of
significant late Cenozoic extensional faulting in the immediate region
implies a strong thermo-mechanical lid that likely suppressed the ascent
of voluminous asthenosphere derived magmas that were hypothetically
sourced from a deep underlying slab window.

## Geothermal implications

The Farallon Plate, Monterey Plate, and slab window scenarios for mantle
lithosphere emplacement all imply a peridotite composition with a
depleted (convecting-mantle) isotopic and trace-element signature.
Though petrographic and geochemical variations can provide information
on the fractionation history, they cannot discriminate between these
potential depleted convecting mantle sources. However, these emplacement
scenarios present potentially distinct thermal structures due to the
large differences in timescales of cooling.

The Farallon-- and Monterey--plate scenarios are qualitatively similar,
with initial emplacement beneath a mid-ocean ridge and cooling on the seafloor. After
subduction and underplating, the cooled oceanic lithosphere
re-equilibrates with an overlying 30 km of forearc crust until the
present, pr for our xenolith samples until the time of entrainment and
eruption. However, the timescales of cooling are significantly different. In
the Farallon-plate scenario, the maximum age of underplating is 70 Ma,
based on the youngest ages of the most pertinent (Sierra de Salinas and
correlative Sn Emigdio-Rand) schist bodies
[@Barth2003; @Grove2003; @Saleeby2007; @Chapman2010]. Seafloor being subducted at that time was 40 Myr old
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

