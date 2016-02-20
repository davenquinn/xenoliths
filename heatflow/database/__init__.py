import numpy as N
from click import echo, secho, style
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import partial, wraps
from contextlib import contextmanager

from ..config import DBNAME
from .models import meta, ModelRun, ModelTracer, ModelProfile

class Database(object):
    def __init__(self, dbname):
        self.engine = create_engine(dbname)

    def execute(self, query):
        a = self.engine.connect()
        a.execute(query)

    def session(self):
        conn = self.engine.connect()
        s = sessionmaker(bind=conn)
        return s()

db = Database(DBNAME)

def drop_tables():
    secho("Dropping database tables", fg='red')
    db.execute("DROP SCHEMA {} CASCADE".format(meta.schema))

def create_tables():
    secho("Creating database tables", fg='green')
    db.execute("CREATE SCHEMA "+meta.schema)
    meta.create_all(db.engine.connect())

def refresh_tables():
    drop_tables()
    create_tables()

class Recorder(object):
    def __init__(self, **kwargs):
        self.session = db.session()

        kw = dict(name=kwargs.pop('name'))

        self.run = (self.session
            .query(ModelRun)
            .filter_by(**kw)
            .first())

        if self.run is None:
            self.run = ModelRun(**kw)
            self.session.add(self.run)

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
            name=step_name, time=t, run=self.run,
            temperature=T, dz=dz)
        self.session.add(v)

    def log(self,message):
        echo(message)

def instrumented(name=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            _ = name
            if _ is None:
                # We get name as first argument
                # passed to wrapped function
                args = list(args)
                _ = args.pop(0)
            rec = Recorder(name=name)
            try:
                return f(rec,*args,**kwargs)
            finally:
                rec.session.commit()
        return wrapper
    return decorator
