from __future__ import division
from uncertainties import ufloat
import numpy as N

# Isotope calculations from McCulloch and Wasserberg, 1978

# Only for the present
# CHUR values from Faure, 2005 pp 199-200
nd_chur_0 = 0.512638 # DePaolo and Wasserberg
sm_nd_chur = 0.1967 # McCulloch and Wasserberg
lam = 6.54e-12

def Epsilon_Nd(row,T=0):
    if T == 0:
        n = row['143Nd/144Nd(0)']
        nd_chur = nd_chur_0
    else:
        n = sample_nd_ratio(row,T)
        nd_chur = correct_nd_ratio(nd_chur_0,sm_nd_chur,T)
    sample = ufloat(n,n*row['std err%']/100)
    return (sample/nd_chur - 1)*1e4

def correct_nd_ratio(nd_ratio_0, sm_nd, time):
    corr = sm_nd*(N.exp(lam*time)-1)
    return nd_ratio_0 - corr

def sample_nd_ratio(row, time):
    """
    Corrects 143Nd/144Nd ratio to a time in the past.
    Uses method from McCulloch and Wasserburg
    """
    return correct_nd_ratio(
        row['143Nd/144Nd(0)'],
        row['147Sm/144Nd'],time)

def sample_sr_ratio(row, time):
    lam = 1.39e-11 # Half life of 87Rb is 48.8 Ga;
    # 27.83% of Rb is 87Rb, which decays to 87Sr
    # which is 7.04% of total Sr (relative to 9.87% 86Sr)
    # all this together makes this number
    factor = row['87Rb/86Sr']*(N.exp(lam*time)-1)
    return row['87Sr/86Sr(0)']-factor

def T_CHUR(row, T=0):
    if T == 0:
        ratio = row['143Nd/144Nd(0)']
        nd_chur = nd_chur_0
    else:
        ratio = sample_nd_ratio(row, T)
        nd_chur = correct_nd_ratio(nd_chur_0,sm_nd_chur,T)
    _ = (ratio-nd_chur)/(row['147Sm/144Nd']-sm_nd_chur)
    # Time expressed in Ga
    return 1/lam*N.log(_+1)*1e-9
