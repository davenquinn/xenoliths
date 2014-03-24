from __future__ import division

from matplotlib.pyplot import figure

def plot(solution):
    fig = figure()
    ax = fig.add_subplot(111)
    line = None
    for sol in solution:
        if line == None:
            line = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()
