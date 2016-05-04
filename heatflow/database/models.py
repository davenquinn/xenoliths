from sqlalchemy import Column, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import Integer, String, Float, Numeric, DateTime

meta = MetaData(schema='thermal_modeling')
Base = declarative_base(metadata=meta)

class ModelRun(Base):
    """
    Table to store data about individual model runs.
    """
    __tablename__ = 'model_run'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    start_time = Column(Numeric) # Ma
    subduction_time = Column(Numeric) # Ma
    underplating_time = Column(Numeric) # Ma
    underplating_duration = Column(Numeric) # Ma
    underplating_depth = Column(Numeric) # km

    run_time = Column(
            DateTime(timezone=True),
            server_default='now()')

    profiles = relationship("ModelProfile", backref='run',
        cascade="delete, delete-orphan")
    tracers = relationship("ModelTracer", backref='run',
        cascade="delete, delete-orphan")

class __shared(object):
    @declared_attr
    def run_id(cls):
        return Column(Integer,
            ForeignKey(ModelRun.id, ondelete='CASCADE'),
            primary_key=True)

class BaseProfile(Base):
    __abstract__ = True
    temperature = Column(
        ARRAY(Float, dimensions=1),
        nullable=False)
    dz = Column(Float, nullable=False)

class StaticProfile(BaseProfile):
    __tablename__ = 'static_profile'
    id = Column(Integer, primary_key=True)
    # Modern heat flow
    heat_flow = Column(Numeric)

class ModelProfile(BaseProfile, __shared):
    __tablename__ = 'model_profile'
    name = Column(String, primary_key=True)
    time = Column(Numeric)

class ModelTracer(Base, __shared):
    __tablename__ = 'model_tracer'
    # Handles cases where we have advection, as
    # the depth may not be constant throughout the
    # model run
    time = Column(Numeric, primary_key=True)
    final_depth = Column(Numeric, primary_key=True)
    depth = Column(Numeric,nullable=False)
    temperature = Column(Float, nullable=False)
