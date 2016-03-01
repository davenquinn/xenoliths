from __future__ import division
from uncertainties import ufloat
import numpy as N

# Isotope calculations from McCulloch and Wasserberg, 1978

# Only for the present
# CHUR values from Faure, 2005 pp 199-200
nd_chur_0 = 0.512638 # DePaolo and Wasserberg
sm_nd_chur = 0.1967 # McCulloch and Wasserberg
lam = -6.54e12

def Epsilon_Nd(row):
    n = row['143Nd/144Nd(0)']
    sample = ufloat(n,n*row['std err%']/100)
    return (sample/nd_chur_0 - 1)*1e4

def T_CHUR(row):
    _ = (row['143Nd/144Nd(0)']-nd_chur_0)/(row['147Sm/144Nd']-sm_nd_chur)
    return 1/lam*N.log(1-_)
