import numpy as N
from click import echo, secho, style
from geotherm.solvers import FiniteSolver
from geotherm.plot import Plotter
from geotherm.units import u

from .config import (
    record_max_depth,
    solver_constraints,
    present)
from .database import db
from .database.models import meta, ModelRun, ModelTracer, ModelProfile

FiniteSolver.set_defaults(
    type="implicit",
    time_step=u(0.5,"Myr"),
    constraints=solver_constraints,
    plotter=Plotter(range=(0,1600)))

class ModelRunner(object):
    trace_depths = u(40,'km'),u(75,'km')
    # Offset used for depth calculations for model tracers.
    # Reset when geotherms are stacked.
    depth_offset = None
    fields = (
        "underplating_duration",
        "underplating_depth",
        "underplating_time",
        "start_time",
        "subduction_time")
    name_base = None
    def __init__(self, **info):
        self._top_depth = u(0,'km')
        for i in self.fields:
            setattr(self,i,None)

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
            v = model.value()
            self.section.profile[:len(v)] = v
        for depth in self.trace_depths:
            self.trace(depth, t=t)

    def finite_solve(self, end_time, **kwargs):
        defaults = dict(
            constraints = (u(0,"degC"), self.section.profile[-1]),
            step_function = self.step_function)

        for k,v in defaults.items():
            if k not in kwargs:
                kwargs[k] = v

        self.log("Initializing finite solver")
        self.log("Constraints")
        labels = ('upper','lower')
        for l,c in zip(labels,kwargs['constraints']):
            self.log("    - "+l,c)
        duration = self.t - end_time
        solver = FiniteSolver(self.section, **kwargs)
        self.set_state(end_time,solver(duration))

    def solve_to_present(self):
        self.finite_solve(present)
        # Record a final step
        self.step_function()
        self.record("final")

    def section_data(self, section):
        # Check if all cells are the same size
        z_ = section.cell_sizes.into('m')
        self.dz = z_[0]
        self.n_cells = int(record_max_depth.into('m')/self.dz)
        assert N.all(z_ == self.dz)
        T = list(section.profile[:self.n_cells].into("degC"))
        return T, self.dz

    def record(self, step_name, section=None, **kwargs):
        t = kwargs.pop("t",self.t).into("Myr")
        if section is None:
            section = self.section

        self.log("Saving profile "+style(step_name, fg='cyan'))

        T, dz = self.section_data(section)
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

        vals = {k:getattr(self,k) for k in self.fields}
        kw.update({k: v.into(
                'km' if k == 'underplating_depth'
                else 'Myr')
            for k,v in vals.items()
            if v is not None})
        kw['type'] = self.name_base
        self.__model = ModelRun(**kw)
        self.session.add(self.__model)

    def trace(self, depth, t=None):

        if self.depth_offset is None:
            _depth = depth
        else:
            _depth = depth - self.depth_offset

        assert _depth >= u(0,'km')

        if t is None: t = self.t

        # Because we are dealing with
        # final section only
        cell = int((_depth-self._top_depth).into('m')/self.dz)
        T = self.section.profile[cell]

        v = ModelTracer(
            run=self.__model,
            time=t.into("Myr"),
            final_depth=depth.into("km"),
            depth=_depth.into("km"),
            temperature=T.into("degC"))
        self.session.add(v)

    def log(self, message, data=None):
        if data is None:
            echo(message)
            return

        width = 30
        start = message+": "
        dt = width-len(start)
        start += " "*dt
        echo(start+style(str(data),fg='green'))

    def __call__(self, *args, **kwargs):
        self.setup_recorder()
        try:
            self.run(*args,**kwargs)
        finally:
            self.session.commit()
