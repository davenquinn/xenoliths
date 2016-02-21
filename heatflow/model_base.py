import numpy as N
from click import echo, secho, style
from geotherm.solvers import FiniteSolver
from geotherm.units import u

from .config import record_max_depth, present
from .database import db
from .database.models import meta, ModelRun, ModelTracer, ModelProfile

class ModelRunner(object):
    def __init__(self, **info):
        self.info = info
        self.trace_depths = u(40,km),u(80,km)

    def run(self):
        pass

    def set_state(self,time,section):
        self.t = time
        self.section = section

    def step_function(self, model=None, **kwargs):
        """
        Step function for finite element solver that records model tracers
        """
        t = self.t
        dt = kwargs.pop('simulation_time', None)
        if dt is not None:
            t -= dt
        if model is not None:
            self.section.profile = model.value()
        for depth in self.trace_depths:
            self.trace(depth, t=t)

    def finite_solve(self, end_time, **kwargs):
        constraints = (u(0,"degC"), u(1450,'degC'))#self.section.profile[-1])
        echo("Initializing finite solver with constraints "
                "{0} and {1}".format(*constraints))

        duration = self.t - end_time
        kwargs['step_function'] = self.step_function

        solver = FiniteSolver(self.section, constraints=constraints, **kwargs)
        self.set_state(end_time,solver(duration))

    def solve_to_present(self):
        self.finite_solve(present)
        # Record a final step
        self.step_function()
        self.record("final")

    def record(self, step_name, section=None, **kwargs):
        t = kwargs.pop("t",self.t).into("Myr")
        if section is None:
            section = self.section

        self.log("Saving profile "+style(step_name, fg='cyan'))

        # Check if all cells are the same size
        z_ = section.cell_sizes.into('m')
        self.dz = z_[0]
        self.n_cells = record_max_depth.into('m')/self.dz

        assert N.all(z_ == self.dz)
        T = list(section.profile[:self.n_cells].into("degC"))

        v = ModelProfile(
            name=step_name, time=t,
            run=self.__model, temperature=T, dz=self.dz)
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

    def trace(self, depth, t=None):

        if t is None: t = self.t

        cell = depth.into('m')/self.dz
        T = self.section.profile[cell]

        v = ModelTracer(
            run=self.__model,
            time=t.into("Myr"),
            depth=depth.into("km"),
            temperature=T.into("degC"))
        self.session.add(v)

    def log(self,message):
        echo(message)

    def __call__(self, *args, **kwargs):
        self.setup_recorder()
        try:
            self.run(*args,**kwargs)
        finally:
            self.session.commit()
