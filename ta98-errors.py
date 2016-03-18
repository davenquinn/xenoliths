from xenoliths import app
from xenoliths.thermometry.results import xenoliths, sample_temperatures
from IPython import embed

with app.app_context():
    data = [sample_temperatures(s,
        calibration_errors=True,
        breakout_errors=True,
        uncertainties=True)
       for s in xenoliths()]
    data = [s['core']['ta98']['sep'] for s in data]
    embed()
