from __future__ import division
import numpy as N

from ...SIMS.models import SIMSMeasurement, average
from ...microprobe.group import get_cations, get_oxides
from ...microprobe.models import ProbeMeasurement
from ...microprobe.models.query import tagged, exclude_bad
from .pyx import pyroxene_form, BKN
from ..thermometers import BKN as BKN_test

from uncertainties.unumpy import log

big10 = "SiO2 TiO2 Al2O3 Cr2O3 FeO MnO MgO CaO Na2O K2O".split()
rare_earths = "La Ce Pr Nd Sm Eu Gd Tb Dy Y Ho Er Tm Yb Lu".split()
minerals = ("opx", "cpx")

def prepare_data(sample):
    probedata = ProbeMeasurement.query.filter(ProbeMeasurement.sample==sample)
    major_elements = tagged(exclude_bad(probedata),"core")
    trace_elements = SIMSMeasurement.query.filter(SIMSMeasurement.sample==sample)

    def prep_oxides(mineral):
        q = major_elements.filter(ProbeMeasurement.mineral == mineral).all()
        avg = get_oxides(q)
        return [avg[k] for k in big10]

    def prep_trace(mineral):
        q = trace_elements.filter_by(mineral=mineral)
        avg = average(q, uncertainties=False)#, normalized=False)
        return [avg[k] for k in rare_earths] # function to array-ize dictionary

    return dict(
        major={k:prep_oxides(k) for k in minerals},
        trace={k:prep_trace(k) for k in minerals})

def ree_pyroxene(sample, pressure=1.5):
    """ Calculate REE temperature
        Chenguang Sun
        Date: 2012-09-16

        Converted to Python from VBScript by Daven Quinn (2014-09-14)
    """

    major_elements = tagged(exclude_bad(ProbeMeasurement.query.filter(ProbeMeasurement.sample==sample)),"core")
    trace_elements = SIMSMeasurement.query.filter(SIMSMeasurement.sample==sample)

    opx = major_elements.filter(ProbeMeasurement.mineral == "opx").all()
    cpx = major_elements.filter(ProbeMeasurement.mineral == "cpx").all()
    T_BKN = BKN(opx,cpx).temperature(pressure) # Two-pyroxene BKN temperature
    assert T_BKN - BKN_test(opx,cpx).temperature(1.5) < 0.0001

    ree_opx = average(trace_elements.filter_by(mineral="opx"), uncertainties=False)#, normalized=False)
    ree_cpx = average(trace_elements.filter_by(mineral="cpx"), uncertainties=False)#, normalized=False)

    keys = "La Ce Pr Nd Sm Eu Gd Tb Dy Y Ho Er Tm Yb Lu".split()
    ree_array = lambda x: N.array([x[k] for k in keys]) # function to array-ize dictionary

    ree_opx = ree_array(ree_opx)
    ree_cpx = ree_array(ree_cpx)

    NA = 602

    kk = 2
    Cali_i = 0

    H2O = 1 # Not sure what this term is or why it is later set to zero...apparently right before major elements in spreadsheet
    H2O = 0.000170685747186617 * H2O**3 - 0.006831778563526 * H2O**2 + 0.109999984719062 * H2O + 0.000971902247238525
    H2O = 0

    #Major = SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O

    DREE = ree_opx/ree_cpx
    #DREE[ree_opx <= 0 and ree_cpx <= 0] = 0

    cpx_site = pyroxene_form(get_cations(cpx, uncertainties=False))
    opx_site = pyroxene_form(get_cations(opx, uncertainties=False))

    #IR = La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Y, Ho, Er, Tm, Yb, Lu
    IR = N.array([1.16, 1.143, 1.126, 1.109, 1.079, 1.066, 1.053, 1.04, 1.027, 1.019, 1.015, 1.004, 0.994, 0.985, 0.977])

    A = (-5.37068370408382) - (-7.13615731281538)
    Ao = 3.56148426371104 * opx_site.m2.Ca + 3.54081780772732 * opx_site.four.Al
    Ac = 4.37096420622614 * cpx_site.four.Al + 1.9813056415739 * cpx_site.m2.Mg - 0.908067851839806 * H2O
    A = A + Ao - Ac

    R0_o = 0.692505524356551 + 0.431788725148506 * opx_site.m2.Ca + 0.227605456716806 * opx_site.m2.Mg
    E_o = -1372.47337291936 + 1854.82137214735 * R0_o - 530.577358996128 * opx_site.m2.Ca

    R0_c = 1.06596147404798 - 0.103654121912384 * cpx_site.six.Al - 0.211803756387744 * cpx_site.m2.Mg
    E_c = -1996.06952151084 + 2271.90977329864 * R0_c

    c = 4 * N.pi * NA

    B_opx = c * E_o * (R0_o/2*(R0_o-IR)**2 - (R0_o-IR)**3/3)
    B_cpx = c * E_c * (R0_c/2*(R0_c-IR)**2 - (R0_c-IR)**3/3)
    Br = (38733.9838585151 - 71864.8736892434 - B_opx + B_cpx)/8.3145

    #Calculate ln(D)-A

    LnD_A = N.log(DREE)-A
    return LnD_A, Br
