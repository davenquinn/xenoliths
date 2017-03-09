"""
    The Steady State Thermal Structure of Eroding
    Orogenic Belts and Accretionary Prisms
    L. H. Royden, jgr, 1993.

"""

from os import path

import numpy as N

from .royden import RoydenModel

__here__ = path.dirname(__file__)

get_fixture = lambda n: path.join(__here__,"test-fixtures",n)


def royden_case():
    """
    Test case for the Royden model using default values.
    """
    royden = RoydenModel(
        #	temperature at the base of the lithosphere (degrees C)
        Tm=1250,
        #   thickness of the lithosphere
        l=125e3,
        #   radiogenic heat production  (W/m3)
        Al=1e-6, #lower plate
        Au=1e-6, #upper plate
        #   heat conductivity in each plate  (W/m.K)
        Kl=2.5, #lower plate
        Ku=2.5, #upper plate
        #   depth to the base of the radiogenic layer (m)
        zr=15e3,
        #   rate of accretion (m/s)
        a=1*1e-3/(365*24*3600),
        #   rate of erosion (m/s)
        e=3*1e-3/(365*24*3600),
        #   rate of under thrusting (m/s)
        v=20.*1e-3/(365*24*3600),
        #   thermal diffusivity  (m2/s)
        alpha=1e-6,
        #   heat flow due to friction on fault (tau*v) (W/m2)
        qfric=15.*1e-3)

    return royden

def matlab_results():
    """ Returns the test fixtures generated with the previous,
        Matlab version of this code.
    """
    return N.loadtxt(get_fixture("temperature_mat"))

def forearc_slice():
    """ A generalization of the Royden test model over the cross-sectional
        area of a forearc.
    """

    royden = royden_case()

    infile = N.loadtxt(get_fixture("interplatetopo"))
    #[xinter,yinter]=textread('interplatetopo','%n%n')

    xinter = infile[:,0]*1e3 #now xinter is in meters
    yinter = -infile[:,1]*1e3 #now yinter is in meters
    #v2=(a-e)/tan(2*pi*phi/360); !!MAKE SURE THIS EQ IS CORRECT

    #initializing:
    model = N.zeros((251*76,3))

    depth = N.linspace(0,150,76)*1e3
    distance = N.linspace(-200,300,251)*1e3
    xv,zv = N.meshgrid(distance, depth)
    h = N.zeros(distance.shape)

    for i in range(len(distance)):
        x = distance[i]
        if x > 0:
            #    dip angle (o)
            #teta=15.*N.pi/180
            #h=x*N.tan(teta)
            for k in range(len(xinter)-2):
                if xinter[k] <=x and x <= xinter[k+1]:
                    n=k

            if xinter[-1] < x:
                igood=len(xinter)-2
            f = (yinter[n+1]-yinter[n])/(xinter[n+1]-xinter[n])
            h[i]=yinter[n]+(x-xinter[n])*f
            if h[0] < 0: h[i] *= -1
    h = N.expand_dims(h,axis=0)
    model = royden(xv,zv,h)
    return model

def test_royden():
    """
    Tests whether Python translation of Royden model produces same
    results as the original MATLAB version.

    Needs input-file interplatetopo that has two columns, first is
    horizontal distance in kilometers, second is vertical distance
    in kilometers
    parameters
       depth: z
       distance along the surface: x
    """
    model = forearc_slice()
    data = matlab_results()
    d = data[:,2].reshape(tuple(reversed(model.shape))).T
    assert d.shape == model.shape
    assert abs(d-model).max() < 0.1

