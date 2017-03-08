import numpy as N
from matplotlib.colors import colorConverter, LinearSegmentedColormap

class ScatterPlotter(object):
    def __init__(self, ax, **kwargs):
        self.ax = ax
        self.kwargs = kwargs

    def plot(self,x,y,**kwargs):
        """
        Simple plot of the data without any contouring
        """
        self.ax.plot(x,y,".",rasterized=True, **kwargs)


    def contour(self, x,y, color="#000000", **kwargs):

        x = N.array(x)
        y = N.array(y)

        # Set up data limits
        minmax = lambda x: (x.min(),x.max())
        k = self.kwargs
        xrange = N.array(k.pop('xrange',minmax(x)))
        yrange = N.array(k.pop('yrange',minmax(y)))
        n = k.pop('n',100)
        nx = k.pop('nx', n)
        ny = k.pop('ny', n)

        # Color scale from transparent to opaque
        opaque = colorConverter.to_rgba(color)
        transparent = colorConverter.to_rgba(color,alpha = 0.0)
        cmap = LinearSegmentedColormap.from_list('cmap',[transparent,opaque],256)

        # cell centers
        centers = lambda v: (v[1:]+v[:-1])/2

        # Compute density function
        h,x_,y_ = N.histogram2d(x,y, (nx,ny), [xrange,yrange])
        # Scatter contour
        CS = self.ax.contourf(centers(x_),centers(y_),h,cmap=cmap, extend='both', **kwargs)

    __call__ = contour
