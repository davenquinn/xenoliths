## Thermometry

Electron-microprobe major-element data is used as the basis for pyroxene
Ca--exchange geothermometry. Several formulations of this reaction are
tested `[Table thermometry]`: BKN [@Brey1990] and TA98 [@Taylor1998] are
two slightly different formulations based on empirical calibration of the two-pyroxene Ca exchange
reaction in simple and natural systems. @Taylor1998 is explicitly calibrated to
account for errors arising from high Al content.
The Ca-in-orthopyroxene (Ca-OPX) thermometer [@Brey1990] is formulated for
use in the absence of clinopyroxene.
Together, these thermometers can query the full range of major-element compositions
seen in the Crystal Knob dataset.

<!--[[thermometry]]-->

#### Error in thermometer calibrations

Core and rim compositions measured on the microprobe are separated to assess within-sample
temperature disequilibrium and late-stage (e.g. eruptive) heating. Analytical errors (caused by
uncertainty in microprobe data) are small, on the order of 5ºC (1$\sigma$).
Other sources of error include the calibration of the thermometer
and potential bias from within-sample disequilibrium. @Taylor1998
reports residuals of calibration of the thermometer to experimental
data which yield total errors of 50-60ºC (1$\sigma$). Unreported calibration errors for the
BKN and Ca-OPX thermometers are likely similar in scale. In practice,
error distributions based on calibration with heterogeneous experimental
samples likely form an upper bound on relative errors. Within-sample scatter in measured temperatures
can be used to estimate the relative error of the thermometer, and the relative
performance of different thermometers can be used to assess the recovery of absolute temperatures.

Within-sample variation in temperatures can be useful in assessing the potential errors
in calculated temperatures. The dataset of pyroxene composition measurements is
grouped by location for thermometry, with a separate temperature calculated
for each individual nearest-neighbor pair of orthopyroxene and clinopyroxene.
Analytical errors are propagated through the calculation.
The resulting distribution of temperatures for grain cores and rims for each sample
(with *n* ranging from 19 to 74 pairs per
group) accounts for within-sample variation and provides an
approximation of measurement precision.

TA98 and BKN temperatures have a strong linear relationship, with BKN
temperature estimates higher by up to 50ºC.
The disparity decreases
towards higher temperatures and conforms to the relationship between
the two thermometers found by @Nimis2010.
This relationship can be expressed as
$\textrm{T}_\textrm{BKN} = 0.9~\textrm{T}_\textrm{TA98} + 145$ for temperatures
in ºC.
@Nimis2010 shows that TA98 performs well against
experimental results in several scenarios and advises its use over BKN.
The Ca-in-OPX thermometer generally yields results coincident with BKN
temperatures (sensibly, as they were calibrated from the same dataset) [@Brey1990].
The Ca-in-OPX thermometer yields remarkably little within-sample scatter, possibly the result of fast diffusion
and complete re-equilibration of small amounts of Ca in orthopyroxene,
or of generally higher stability of this more refractory phase against late magmatic modification. <!-- *** --->

Average TA98 temperatures range from 957 to 1063ºC for cores and
955 to 1054ºC for rims `[Table thermometry]`.
CK-2 core temperatures indicate more complete
equilibration, with a standard deviation of only 2.3ºC (compared
with 8.2-12.4ºC for all other samples). Temperatures are distributed roughly normally
for most samples, but outlying clusters of measurements in CK-4 and CK-6 may indicate
two-pyroxene major element disequilibrium at millimeter scale.
In CK-4, a few grain cores with TA98
temperatures of 1100ºC are likely related to late-stage diffusion during
entrainment and eruption.
Within-sample temperature variability is a relatively minor feature: for grain cores in all samples,
the mean of pairwise analyses is within a few degrees
of the temperature calculated for average compositions of pyroxene phases across the sample.
This implies that the bulk of the temperature signature
is based on the equilibrium state of the sample.

#### Rim temperatures

Rim temperatures (measured ~10 µm from grain edges) are generally higher than
core temperatures, although the level of disparity varies widely between samples.
CK-2 shows only modestly elevated rim temperatures, while CK-3 and CK-6
show significant scatter to temperatures ~180 ºC higher than grain cores
(CK-5 and CK-7 contain a few measurements of this type as well).
High and variable rim compositions may be related to fluid infiltration
during entrainment and eruption of the xenoliths, but with significant
mobilization of cations was limited to grain rims. CK-4, which shows high core temperatures
and the most significant petrographic evidence of melt interaction, has no
high-temperature rim compositions, implying more sustained equilibration with the Crystal
Knob melt.

#### Two temperature cohorts

The samples can be divided into two clear cohorts based on equilibration temperatures. A cooler
group of samples, with a distribution of grain core temperatures centered at ~970ºC (TA98), contains CK-2, CK-5, and CK-7.
A hotter group, with a mean temperature of ~1050ºC (TA98) contains samples CK-3, CK-4, and CK-6.
This division between these two groups is robust and apparent in all thermometers, as well as in
other geochemical data.
The high-temperature samples show significantly higher levels of REE depletion, as well
as some amount of re-enrichment in LREEs. They also contain chromian spinels, which are a product of increased
levels of melt extraction.
This temperature distribution may signify sourcing of these two sets of xenoliths from different
depths within a magmatic system. Throughout this paper, the samples are color-coded, with
blue-green corresponding to the low-temperature array, and red-yellow representing
the high-temperature samples.

<!--[[temp_comparisons]]-->
<!--[[temp_summary]]-->

### REE-in-pyroxene thermometry

We use the @Liang2013 REE-in-two-pyroxene thermometer to estimate the
equilibration temperature of the samples using an independent system.
The relative immobility of REEs allows assessment
of equilibrium temperatures over longer timescales than those queried
with two-pyroxene cation exchange thermometry.

\renewcommand{\D}{D^\mathrm{opx/cpx}}

Rare-earth abundances are compiled for SIMS measurements of
pyroxene phases in contact (2--3 pairs) for each xenolith sample.
A two-pyroxene equilibrium is calculated for each REE element and Y,
equivalent to $T_i [K] = B_i (\ln(\D_i)-A_i)^{-1}$.
These per-element equilibration temperatures are shown in `Figure ree_thermometry`.
The best-fitting line from the origin through each point
in $B$ vs. $\ln(\D)-A$ space
(using a robust regression with a Tukey biweight norm) yields
the equilibrium temperature for each sample.
Significant outliers from the fit are excluded from the thermometry.

### Disequilibrium between phases

CK-3 shows disequilibrium in La only, while CK-5 and CK-7 have disequilibrium
in several of the LREEs. 
Sample CK-4 shows major disequilibrium in the light and medium REEs, with only
elements heavier than Ho retaining an equilibrium signature.

The pattern of disequilibrium in sample CK-4 suggests that $\D$ for the LREEs
is larger than anticipated relative to that for HREEs. This is perhaps
due to low clinopyroxene modes in the harzburgite CK-4. The shape of this
disequilibrium relationship may be traceable to the parabolic nature
of mineral-melt partition curves for both pyroxene phases, which are
incompletely modeled by a linear relationship when offset [@Sun2012;@Blundy2003].
Alternatively, low clinopyroxene modes in the harzburgite CK-4 could be
result in more being incorporated into orthopyroxene, showing incomplete REE
diffusion throughout the sample. This is consistent with late re-enrichment
in LREEs from the Crystal Knob source magma.

All samples except CK-6 and CK-7 show results off the linear trendline for Eu.
This distinct disequilibrium was also found in calibration by @Sun2012, and is
dependent on the oxygen fugacity (and \ce{Eu^{2+}}/\ce{Eu^{3+}} ratio of the
host magma. The strength of these disequilibria suggests that a significant
amount of \ce{Eu^{2+}} exists in these samples and that it is strongly
partitioned between orthopyroxene and clinopyroxene. Moreover, the dataset
suggests an incorrect partition coefficient, with Eu favoring orthopyroxene at
a factor of up to 10. Since this disequilibrium exists between pyroxenes, it is
unlikely to correspond to fractionation into plagioclase, the usual culprit for
Eu depletions in melt residues. However, this could be the case if quicker
diffusion of Eu out of clinopyroxenes is invoked, and the samples were never
fully equilibrated. The exact kinetics of this scenario are unclear, but it is
likely that REE equilibrium was achieved in a highly reducing environment
(Asimow and Blundy, personal communication) !!, or Eu was rapidly and
differentially diffused into the Crystal Knob melt just prior to eruption.
Evaluating these scenarios is more difficult due to the low Eu counts
measured by ion-microprobe techniques.

Generalized LREE disequilibrium could be explained by
a fossil heating event that was retained only in the large-ion lithophile elements due to their
slow diffusion rates. This must have happened prior to re-equilibration in major elements.
Alternatively, partition coefficients for LREE and Eu
could have been modified by an unusual late-stage melt interaction
favoring the extraction of LREE and Eu from clinopyroxene. <!-- and driving up the relative abundance of LREE in
orthopyroxene -->
Overall, disequilibrium patterns in REE between pyroxenes allude to possible
eruptive effects, poorly understood equilibrium partition coefficients 
(for instance, due to reducing mantle conditions), and incomplete linearizing assumptions
in the @Liang2013 thermometer. Disentangling these effects
is beyond the scope of this work but presents several opportunities for further study.
Even in samples (such as CK-4) with LREE disequilibrium, temperature estimates anchored
by HREE perform well as measured against major-element thermometry.

### Significance of temperature estimates

Rare-earth exchange thermometry shows the samples as divided into
the same two groupings of temperatures as those found by major-element
thermometry. Temperatures measured for the low-temperature cohort are
most comparable to the TA98 results `[Figure ree_thermometry]`.
Given that the TA98 method has been
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


