Hi Daven,

Here are my comments, such as I am able to give. I mostly stuck, as requested, to the petrological bits.

1. Page 6, analytical methods: 15 kV is an accelerating potential, not a probe current. You need to check with Chi to find out the actual probe current (perhaps 25 nA?), and you should give the beam size (i.e, focused or diffused) and the counting times on- and off-peak.

A focused beam, 25 nA, and 20 seconds on-peak and 10 seconds off-peak.
DONE

2. Line 287: “high Mg#s indicative of fertile compositions” … huh? That seems backwards on one end of the sentence or the other.

DONE

3. Lines 288-290: Why do you put a “however” between low Mg# in cpx and high Fe content in olivine for CK-6? Those seem quite consistent, not logically opposed. Also, I would avoid “the sample has high abundances of iron” when talking about mineral chemistry because that sounds like a statement about whole-rock composition. In general, I get to the end of section 2.4.1 rather confused about sample CK-6.

Need to reformulate to emphasize:
- CK-6 is an outlier
- Fertile composition seems to be gained by refertilization
- Both initial residue and refertilizing agent were likely rather evolved, given high-iron composition of mineral components.

4. Section 2.4.2: it would be suitable to comment here or later on the degree to which mineral chemistry and mineral modes are correlated, and whether CK-6 is an outlier from said correlations.

5. Lines 342-343: Confirm that you used a *shatterbox* to get 150-300 micron grains? Are you sure it wasn’t a jaw crusher and disk mill? Shatterbox is for making superfine (≤1 micron) powders, I think… Also, confirm 35-45 grams per sample, not 35-45 mg? Really? A gram of 300 micron cpx crystals is about 22,000 grains…

DONE

6. Lines 347-348: The model numbers of the mass spectrometers are  VG 54 and VG 354, not the other way around.

7. Line 364: Again for SIMS, 9 kV is not a beam flux measurement. It is an accelerating potential. Check with Yunbin for actual beam current number.

15-30 nA beam current.

8. Smith and Asimow 2005 reference, the paper number is Q02004, which the journal may want you to put in the bibliography.

DONE

9. Line 398: It is pretty important to state whether there is any residual garnet in the model, because this will strongly influence the Er-Lu concentrations. It is hard to believe that starting at 2 GPa and starting at 3 GPa you get the same results in this regard. Note that in alphaMELTS, unless you set the ALPHAMELTS_OLD_GARNET flag, you get Peter Luffi’s corrected garnet model, which gives the right garnet compositions but displaces the spinel-garnet lherzolite transition down to ~1.7 GPa. Also, you should say what trace element partition coefficient set you used, because alphaMELTS gives you some control over this...

DONE

10. Lines 413-414: I don’t know what you mean by “re-enrichment may be better modeled as a fractional process”. Fractional how? What phase is fractionated? This needs clarification.

Excised.

11. Line 435: What do you mean by “to form abyssal peridotite” … these are not abyssal peridotites since you didn’t dredge them from the abyss. Do you mean “ by a process similar to that which is thought to be recorded in abyssal peridotites”?

12. Lines 439-441: I don’t think the host magma can be the contaminant. If you gave it enough time to react and homogenize, it would reset the two-pyroxene REE thermometer and you wouldn’t get lithospheric temperatures at all. And Ca should reset faster than REE.

DONE

13. Line 534: Personal communications have come to be seen as pretty bad form by editors. Better if you explain the logic that Jon and I used to reach that conclusion so that it is all upfront in the paper. I don’t actually remember making that statement, but when I did, did I explain myself?

14. Line 578: How did 87/86 of 0.7023-0.7024 become 0.7029? How did eNd of 10.3-11 become 10? The values gives in the text here seem like reference DMM values, not the actual sample suite, which is more depleted than average DMM.

Done

15. Line 591: “Volatile” is the wrong word here. You have no information on volatiles (H2O, CO2, F, Cl, S). Do you mean “incompatible”? Not the same.

16. Lines 590 and 597: Once again you seem to have things backwards with respect of Mg# and depletion. *High* Mg# indicates depletion, right?

17. Paragraph at line 605-613 is out of sequence. It depends on depth constraints not yet developed. Needs to be moved later … unless you explicitly state the assumption that increasing temperature corresponds to increasing depth. If it is true, however, it is an inverted depletion gradient compared to what you get from decompression melting, unless the melting episodes were unrelated in space and time. It is more like what you get from flux melting above a slab due to fluid influx from below.

18. Line 626: This is not a geothermal gradient. It is a hydrostatic gradient.

19. Line 630-631: The plagioclase-spinel peridotite transition is a strong function of composition. In Al-depleted and Cr-enriched samples (like the harzburgites), residual plagioclase may never occur at all and Cr-rich spinel may persist at any pressure. Unfortunately, you can’t just quote a standard reference depth for limit of spinel stability in generic peridotites. You need to run thermocalc or Perple_X or MELTS on the actual bulk composition. Sadly, MELTS can’t really handle the Cr effect. There is a calibration of Perple_X that can, to some degree. Everything you say about the spinel-garnet transition in the next paragraph is true of spinel-plagioclase.

20. Line 1207: section number missing.

 On the whole, this is a remarkable piece of work. Well done.

— P

