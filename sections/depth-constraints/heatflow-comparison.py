import numpy as N
from functools import partial
from sys import argv
from xenoliths import app, db
from matplotlib.pyplot import figure
from paper import plot_style
from geotherm.solvers import steady_state, u
# section used for thermal modeling of database sections
from heatflow.calc import steady_state_section as section
from matplotlib.cm import get_cmap

q = """
    SELECT dz,
        heat_flow,
        temperature
    FROM thermal_modeling.static_profile
    WHERE heat_flow < 105 AND heat_flow > 85
   """

with app.app_context():
    profiles = db.session.execute(q).fetchall()

fig = figure(figsize=(4,4),dpi=300)
ax = fig.add_subplot(111)
ax.invert_yaxis()

def plot_heat_curve(heat_flow, A, **kwargs):
    # Change crustal heat generation
    section.layers[0].material.heat_generation = u(A, "uW/m**3")
    s = steady_state(section,u(float(heat_flow),"mW/m**2"))
    ax.plot(
        s.profile.into('degC'),
        s.cell_centers.into('km'),
        **kwargs)

cmap = get_cmap('Reds', 3)
for i, (dz, heat_flow, T) in enumerate(profiles):
    cells = N.arange(len(T))*dz+dz/2
    Z = cells/1000

    ax.plot(T,Z,color='#aaaaaa')

    c = cmap(i)
    fn = partial(plot_heat_curve, heat_flow,
                 color=c, zorder=-20)
    fn(1)
    fn(1.5)
    fn(2)


ax.set_xlim([700,1300])
ax.set_ylim([60,20])

fig.savefig(argv[1],bbox_inches='tight')
