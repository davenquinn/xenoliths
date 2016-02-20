import numpy as N
from click import echo, secho, style

from .models import meta, ModelRun, ModelTracer, ModelProfile

class Recorder(object):
    def __init__(self, db, **kwargs):
        self.session = db.session()
        kw = dict(name=kwargs.pop('name'))

        run = (self.session
            .query(ModelRun)
            .filter_by(**kw)
            .first())
        if run is not None:
            secho("Deleting data from previous run", fg='red')
            self.session.delete(run)
            self.session.commit()

        self.run = ModelRun(**kw)
        self.session.add(self.run)

    def write_trace(self, depth, time, temperature):
        v = ModelTracer(
            run=self.run,
            time=time.into("Myr"),
            depth=depth.into("km"),
            temperature=temperature.into("degC"))
        self.session.add(v)

    def __call__(self, step_name, section, **kwargs):
        if "t" in kwargs:
            t = kwargs["t"].into("Myr")

        self.log("Saving profile "+style(step_name, fg='cyan'))

        # Check if all cells are the same size
        z_ = section.cell_sizes.into('m')
        dz = z_[0]
        assert N.all(z_ == dz)
        T = list(section.profile.into("degC"))

        v = ModelProfile(
            name=step_name, time=t, run=self.run, temperature=[1], dz=dz)
        self.session.add(v)

    def log(self,message):
        echo(message)
