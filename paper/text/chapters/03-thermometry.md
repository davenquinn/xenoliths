## Thermometry

Electron-microprobe major-element data is used as the basis for pyroxene
Ca--exchange geothermometry. Several formulations of this reaction are
tested \tabref{thermometry}: BKN [@Brey1990] and TA98 [@Taylor1998] are
formulated based on empirical calibration of the two-pyroxene Ca exchange
reaction in simple and natural systems. @Taylor1998 is explicitly calibrated to
account for errors arising from high Al content.
The Ca-in-orthopyroxene (Ca-OPX) thermometer [@Brey1990] is formulated for
use in the absence of clinopyroxene.
Together, these thermometers can query the full range of major-element compositions
seen in the Crystal Knob dataset.

<!--[[thermometry]]-->

Core and rim measurements are separated to assess within-sample
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

Per-sample temperature distributions are
constructed by calculating a separate temperature for each individual nearest-neighbor
pair of orthopyroxene and clinopyroxene.
Analytical errors are propagated through the calculation.
The resulting distribution of temperatures (with *n* ranging from 19 to 74 pairs per
group) accounts for within-sample variations and provides an
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
The Ca-in-OPX thermometer generally yields results in between BKN and TA98,
with little within-sample scatter, possibly the result of fast diffusion
of small amounts of Ca in orthopyroxene. <!-- *** --->

Average TA98 temperatures range from 957 to 1063ºC for cores and
955 to 1054ºC for rims \tabp{thermometry}.
CK-2 core temperatures indicate more complete
equilibration, with a standard deviation of only 2.3ºC (compared
with 8.2-12.4ºC for all other samples). Temperatures are distributed roughly normally
for most samples, but outlying clusters of measurements in CK-4 and CK-6 may indicate
disequilibrium at millimeter scale.
In CK-4, a few grain cores with TA98
temperatures of 1100ºC are likely related to late-stage diffusion during
entrainment and eruption.
High and variable rim compositions may also be related to the eruption event.
Several samples show a wide spread rim temperatures, perhaps
indicating differential exposure to interstital fluids.
This internal variability is minor: for grain cores in all samples,
the mean of pairwise analyses is within a few degrees
of the temperature calculated by averaging all pyroxenes across the sample.
This implies that the bulk of the temperature signature
is based on the equilibrium state of the sample.

The samples show an apparent bimodal
distribution in equilibration temperature, forming distinct groups
centered at 970ºC and 1060ºC (TA98) \figref{temp_summary}.
The cooler group contains CK-2, CK-5, and CK-7, while the hotter
contains CK-3, CK-4, and CK-6.
This division between these two groups is robust and apparent in all thermometers.
The high-temperature samples show re-enrichment in LREEs and contain chromian spinels.
This temperature distribution may signify two distinct depths of origin for
the studied xenoliths. Throughout this paper, the samples are color-coded, with
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


- Calculate a per-element equilibrium temperature
- Best fitting line from zero through the data cloud gives sample
  equilibrium temperature

- Robust regression using a Tukey biweight norm


Sample CK-4 shows major disequilibrium in the light and medium REEs, with only
elements heavier than Ho retaining an equilibrium signature.

- In some samples, notably CK-3 and CK-4, LREE show much higher
  equilibration temperatures than HREE
- CK-4 had excess LREE added, causing re-equilibration of LREEs
- This occurred to a lesser extent with CK-3
- Change in temperature?
  - A fossil heating event that was retained due to the large size of LILE
- Due to kinetics of two thermometers, this must have happened before
  re-equilibration of major elements (right??)
- Change in partition coefficients due to other means
  - Some weird melt interaction favoring extraction of LREE from
    clinopyroxene and driving up relative abundance of LREE in
    orthopyroxene

- Europium disequilibrium
  - interesting sidebar to REE thermometry
  - distinct disequilibrium in Eu
  - favors Eu in Opx by a factor of 10
  - different partition coefficient for Eu
  - Eu, because of its two oxidiation states, can behave differently
  - suggests a significant amount of Eu 2+ exists in the samples
  - much more reducing environment in general (Asimow and Blundy,
    personal communication)

<!-- (more descriptive text here?) -->

