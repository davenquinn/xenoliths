"""
Solver for steady-state forearc geotherm in an accretionary wedge.

The Steady State Thermal Structure of Eroding
     Orogenic Belts and Accretionary Prisms
     L. H. Royden, JGR, 1993.

Translated from MATLAB to Python by Daven Quinn, 2014
"""

from __future__ import division, print_function
import numpy as N
from numpy import log, pi, exp, linspace, sign
from scipy.special import erf

def i2erfc1(x):
    return (0.25+0.5*x**2)*erfc1(x)-x*exp(-x**2)/(2*N.sqrt(pi))

def ierfc1(x):
    return -x*erfc1(x)+exp(-x**2)/N.sqrt(pi)

def erfc1(x):
    return 1 - erf(x)

class RoydenModel(object):
    defaults = dict(
        Tm=1250,
        l=125e3,
        Al=1e-6, #lower plate
        Au=1e-6, #upper plate
        Kl=2.5, #lower plate
        Ku=2.5, #upper plate
        zr=15e3,
        a=1*1e-3/(365*24*3600),
        e=3*1e-3/(365*24*3600),
        v=20.*1e-3/(365*24*3600),
        alpha=1e-6,
        qfric=15.*1e-3)

    def __init__(self,**kwargs):
        """
        Parameters:
            Tm    ... temperature at the base of the lithosphere (degrees C)
            l     ... thickness of the lithosphere
            Al    ... heat production in the lower plate (W/m3)
            Au    ... heat production in the upper plate (
            Kl    ... heat conductivity in the lower plate  (W/m.K)
            Ku    ... heat conductivity in the upper plate  (W/m.K)
            zr    ... depth to the base of the radiogenic layer (m)
            a     ... rate of accretion (m/s)
            e     ... rate of erosion (m/s)
            v     ... rate of underthrusting (m/s)
                      relative to (x,z) = (0,0) (m/s)
            alpha ... thermal diffusivity  (m2/s)
            qfric ... heat flow due to friction
                      on fault (tau*v) (mW/m2)
        """
        self.vfunc = N.vectorize(self.royden, excluded="self")

        self.args = {k: kwargs.pop(k,v)\
            for k,v in self.defaults.items()}

        names = "Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric".split(",")
        Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric = \
            tuple(self.args[i] for i in names)

        self.To = Tm+Al*zr*(2*l-zr)/(Kl*2)
        self.fa_ = N.array([e,a])/N.sqrt(2*alpha*abs(e-a))

    def royden(self,x,z,h):
        """
        parameters
            x: distance along the surface
            z: depth
            h: depth of subduction interface
        """
        # 1. calculate the temperature in the foreland (x<0)
        z-=h

        names = "Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric".split(",")
        Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric = \
            tuple(self.args[i] for i in names)

        if x <=  0:
            Tl = (self.To*z)/l-(Al*z**2)/(Kl*2)
            if z >=  zr:
                Tl = Tl+(Al*(z-zr)**2)/(Kl*2)
            return Tl

        # calculate the temperature for (x>0)

        res = self.fa_*N.sqrt(h)
        if a < e:
            d,b = tuple(complex(0,i) for i in res)
        else:
            d,b = tuple(complex(i,0) for i in res)

        g = h*N.sqrt(v)/(2*N.sqrt(alpha*x))
        gg = 3*pi*g/8.
        bb = b/2.
        yr2 = zr*g/h+bb*(b-d)/g

        b1 = d*ierfc1(b)-b*ierfc1(d)
        b2 = (Ku/Kl)*(b-d)*(-d*erfc1(b)-ierfc1(d))
        b3 = ierfc1(b*(b-d)/g)
        b4 = bb*(b-d)/g**2
        b5 = -g*erfc1(b*(b-d)/g)
        b6 = 1+qfric*l/(Kl*self.To)

        c1 = (Au/Ku)*(d**2-b**2)/(((b-d)**2)*(1+2*d**2))
        c2 = (Au/Ku)*(i2erfc1(b)-((1+2*b**2)/(1+2*d**2))*i2erfc1(d))
        c3 = (Au/Kl)*(-2*b)/((b-d)*(1+2*d**2))
        c4 = (Au/Kl)*(b-d)*(-ierfc1(b)-(4*b/(1+2*d**2))*i2erfc1(d))
        c5 = -(Al/Kl)*(bb**2*(b-d)**2)/g**4
        c6 = (Al/Kl)*i2erfc1(b*(b-d)/gg)
        c7 = -(Al/Kl)*(2*bb*(b-d))/g**2
        c8 = -(Al/Kl)*(gg*ierfc1(b*(b-d)/gg))

        b_ = (b1*b5-b2*b3)
        c_ = (c4*c6-c2*c8)

        if z < 0:
            # Upper plate
            Bu = (b4*b5-b3*b6)/b_
            Cu = (c1*c8-c5*c8-c3*c6+c7*c6)/c_

            yu = (z/h)*(b-d)+b

            Tu = (h/l)*Bu*(d*ierfc1(yu)-yu*ierfc1(d))\
                 + Au*h**2/(Ku*self.To*2)*((d**2-yu**2)/((b-d)**2*(2*d**2+1))\
                 + Cu*(i2erfc1(yu)-((2*yu**2+1)/(2*d**2+1))*i2erfc1(d)))
            return (Tu * self.To).real
        else:
            Bl = (b4*b2-b1*b6)/b_
            Cl = (c2*c7-c2*c3-c4*c5+c4*c1)/c_

            _ = (z/h)*g
            yl = _+b*(b-d)/g
            yl1 = 3*N.pi/8*_+b*(b-d)/gg
            yl2 = _+bb*(b-d)/g

            Tl = (h/l)*((yl2/g)+Bl*ierfc1(yl))\
                 + (Al*h**2/(Kl*self.To*2))*(Cl*i2erfc1(yl1)-(yl2/g)**2)
            if yl2.real > yr2.real:
                Tl += (Al*h**2/(Kl*self.To*2))*((yl2-yr2)/g)**2
            return (Tl * self.To).real

    def __call__(self,*args):
        """
        parameters
            x: distance along the surface
            z: depth
            h: depth of subduction interface
        """
        return self.vfunc(*args)
