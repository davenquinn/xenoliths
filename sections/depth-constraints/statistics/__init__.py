from pickle import load
from scipy.stats import gaussian_kde

def barometer_kernel_density(depth):
    return gaussian_kde(depth, 0.1)

def load_data(datafile):
    with open(datafile) as f:
        return load(f)

