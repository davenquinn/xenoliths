import numpy as N
from click import echo, secho, style

from .config import record_max_depth
from .database import db
from .database.models import meta, ModelRun, ModelTracer, ModelProfile

class ModelRunner(object):
    def __init__(self, **info):
        self.info = info

    def run(self):
        pass

    def record(self, step_name, section, **kwargs):
        if "t" in kwargs:
            t = kwargs["t"].into("Myr")

        self.log("Saving profile "+style(step_name, fg='cyan'))

        # Check if all cells are the same size
        z_ = section.cell_sizes.into('m')
        dz = z_[0]
        n_cells = record_max_depth.into('m')/dz

        assert N.all(z_ == dz)
        T = list(section.profile[:n_cells].into("degC"))

        v = ModelProfile(
            name=step_name, time=t,
            run=self.__model, temperature=T, dz=dz)
        self.session.add(v)

    def setup_recorder(self):
        self.session = db.session()
        kw = dict(name=self.name)

        model = (self.session
            .query(ModelRun)
            .filter_by(**kw)
            .first())
        if model is not None:
            secho("Deleting data from previous run", fg='red')
            self.session.delete(model)
            self.session.commit()

        self.__model = ModelRun(**kw)
        self.session.add(self.__model)

    def trace(self, depth, time, temperature):
        v = ModelTracer(
            run=self.__model,
            time=time.into("Myr"),
            depth=depth.into("km"),
            temperature=temperature.into("degC"))
        self.session.add(v)

    def log(self,message):
        echo(message)

    def __call__(self, *args, **kwargs):
        self.setup_recorder()
        try:
            self.run(*args,**kwargs)
        finally:
            self.session.commit()
