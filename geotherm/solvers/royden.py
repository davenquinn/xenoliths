"""
Solver for steady-state forearc geotherm above a subducting slab.

The Steady State Thermal Structure of Eroding
     Orogenic Belts and Accretionary Prisms
     L. H. Royden, JGR, 1993.

Translated from Matlab by Daven Quinn
"""

from __future__ import division, print_function
from numpy import log, pi, exp, sqrt, linspace

def i2erfc1(x):
    return (0.25+0.5*x**2)*erfc1(x)-x*exp(-x**2)/(2*sqrt(pi))

def ierfc1(x):
    return -x*erfc1(x)+exp(-x**2)/sqrt(pi)

def erfc1(x):
    return 1 - erf1(x)

def erf1(x):
    if imag(x) ~= 0:
        return complex(0,2*dawson(imag(x))/(sqrt(pi)*exp(-imag(x)**2)))
    elif real(x) <0:
        return complex(-gammp(0.5,x**2),0)
    else:
        return complex(gammp(0.5,x**2),0)

def royden(x,z,h,Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric):
    """
    %	parameters
    %
    %   depth: z
    %   distance along the surface: x
    %	Tm ... temperature at the base of the lithosphere (degrees C)
    %   l  ... thickness of the lithosphere
    %   Al ... heat production in the lower plate (W/m3)
    %   Au ... heat production in the upper plate (
    %   Kl ... heat conductivity in the lower plate  (W/m.K)
    %   Ku ... heat conductivity in the upper plate  (W/m.K)
    %   zr ... depth to the base of the radiogenic layer (m)
    %   a  ... rate of accretion (m/s)
    %   e  ... rate of erosion (m/s)
    %   v  ... rate of under thrusting (m/s) relative to (x,z) = (0,0) (m/s)
    %   alpha ... thermal diffusivity  (m2/s)
    %   qfric ... heat flow do to friction on fault (tau*v) (mW/m2)
        To = Tm+Al*zr*(2*l-zr)/(Kl*2)
    """
    # 1. calculate the temperature in the foreland (x<0)

    print('Starting with x={0}'.format(x))

    if x <=  0:
        Tl = (To*z)/l-(Al*z**2)/(Kl*2)
        if z >=  zr:
            Tl = Tl+(Al*(z-zr)**2)/(Kl*2)
        return Tl

    # calculate the temperature for (x>0)
    if a < e:
        d = complex(0.,e*sqrt(h)/sqrt(2*alpha*(e-a)))
        b = complex(0.,a*sqrt(h)/sqrt(2*alpha*(e-a)))
    else:
        d = complex(e*sqrt(h)/sqrt(2*alpha*(a-e)),0.)
        b = complex(a*sqrt(h)/sqrt(2*alpha*(a-e)),0.)

    g = h*sqrt(v)/(2*sqrt(alpha*x))
    gg = 3*pi*g/8.
    bb = b/2.
    yr2 = zr*g/h+bb*(b-d)/g

    b1 = d*ierfc1(b)-b*ierfc1(d)
    b2 = (Ku/Kl)*(b-d)*(-d*erfc1(b)-ierfc1(d))
    b3 = ierfc1(b*(b-d)/g)
    b4 = bb*(b-d)/g**2
    b5 = -g*erfc1(b*(b-d)/g)
    b6 = 1+qfric*l/(Kl*To)
    Bl = (b4*b2-b1*b6)/(b1*b5-b2*b3)
    Bu = (b4*b5-b3*b6)/(b1*b5-b2*b3)

    c1 = (Au/Ku)*(d**2-b**2)/(((b-d)**2)*(1+2*d**2))
    c2 = (Au/Ku)*(i2erfc1(b)-((1+2*b**2)/(1+2*d**2))*i2erfc1(d))
    c3 = (Au/Kl)*(-2*b)/((b-d)*(1+2*d**2))
    c4 = (Au/Kl)*(b-d)*(-ierfc1(b)-(4*b/(1+2*d**2))*i2erfc1(d))
    c5 = -(Al/Kl)*(bb**2*(b-d)**2)/g**4
    c6 = (Al/Kl)*i2erfc1(b*(b-d)/gg)
    c7 = -(Al/Kl)*(2*bb*(b-d))/g**2
    c8 = -(Al/Kl)*(gg*ierfc1(b*(b-d)/gg))
    Cl = (c2*c7-c2*c3-c4*c5+c4*c1)/(c4*c6-c2*c8)
    Cu = (c1*c8-c5*c8-c3*c6+c7*c6)/(c4*c6-c2*c8)


    yl = (z/h)*g+b*(b-d)/g
    yl1 = (z/h)*gg+b*(b-d)/gg
    yl2 = (z/h)*g+bb*(b-d)/g
    yu = (z/h)*(b-d)+b

    Tl = (h/l)*((yl2/g)+Bl*ierfc1(yl))+(Al*h**2/(Kl*To*2))*(Cl*i2erfc1(yl1)-(yl2/g)**2)

    if real(yl2) > real(yr2):
        Tl = Tl+(Al*h**2/(Kl*To*2))*((yl2-yr2)/g)**2

    Tl = Tl*To
    Tu = sum([(h/l)*Bu*(d*ierfc1(yu)-yu*ierfc1(d)),
              (Au*h**2/(Ku*To*2))*((d**2-yu**2)/((b-d)**2*(2*d**2+1)),
              Cu*(i2erfc1(yu)-((2*yu**2+1)/(2*d**2+1))*i2erfc1(d)))])

    Tu = Tu*To

    if z < 0: return Tu
    else: return Tl

def dawson(x):
    NMAX = 6
    H = 0.4
    A1 = 2/3
    A2 = 0.4
    A3 = 2/7

    i = linspace(1,NMAX,NMAX)
    c = exp(-((2*i-1)*H)**2)

    if abs(x) < 0.2:
      x2 = x**2
      return x*(1-A1*x2*(1-A2*x2*(1-A3*x2)))

    xx = abs(x)
    n0 = 2*round(0.5*xx/H)
    xp = xx-n0*H
    e1 = exp(2.*xp*H)
    e2 = e1**2
    d1 = n0+1
    d2 = d1-2
    sum_ = 0

    for i in range(NMAX):
        sum_ = sum_ + c[i]*(e1/d1+1/(d2*e1))
        d1 = d1+2
        d2 = d2-2
        e1 = e2*e1

    return 0.5641895835*abs(exp(-xp**2))*sign(x)*sum_

def gammp(a,x):
    ITMAX = 200
    EPS = 3e-7
    if x < 0 or a <= 0:
        raise ArgumentError('Bad arguments')

    if x < (a+1):
        gln = gammln(a)
        if x < 0: raise Exception('x < 0 in gser')
        elif x == 0: return 0
        ap = a
        _sum = 1/a
        del = _sum
        for n in range(ITMAX):
            ap = ap+1
            del = del*x/ap
             _sum = _sum+del
            if abs(del) < abs(_sum)*EPS:
                break
        if n == ITMAX-1:
            raise Exception('a too large, ITMAX too small in gser')
        return _sum*exp(-x+a*log(x)-gln)

    FPMIN = 1e-30
    gln = gammln(a)
    b = x+1-a
    c = 1/FPMIN
    d = 1/b
    h = d
    for i in range(ITMAX):
        an = -(i+1)*((i+1)-a)
        b = b+2.
        d = an*d+b
        if abs(d) < FPMIN: d = FPMIN
        c = b+an/c
        if abs(c) < FPMIN: c = FPMIN
        d = 1/d
        del = d*c
        h = h*del
        if abs(del-1) < EPS: break

    if i == ITMAX-1:
        raise Exception('a too large, ITMAX too small in gcf')

    gammcf = exp(-x+a*log(x)-gln)*h
    return 1-gammcf

def gammln(xx):
    cof = [
        76.18009172947146,
        -86.50532032941677,
        24.01409824083091,
        -1.231739572450155,
        0.1208650973866179e-2,
        -.5395239384953e-5]
    stp = 2.5066282746310005

    x = xx
    y = x
    tmp = x+5.5
    tmp = (x+0.5)*log(tmp)-tmp
    ser = 1.000000000190015
    for c in cof:
        y = y+1
        ser = ser+c/y
    return tmp+log(stp*ser/x)
