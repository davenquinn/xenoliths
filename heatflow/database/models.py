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
    plate_creation = Column(Numeric) # Ma
    subduction_start = Column(Numeric) # Ma
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
    @declared_attr
    def time(cls):
        return Column(Numeric, primary_key=True)

class ModelProfile(Base, __shared):
    __tablename__ = 'model_profile'
    name = Column(String, nullable=False)
    temperature = Column(
        ARRAY(Float, dimensions=1),
        nullable=False)
    dz = Column(Float, nullable=False)

class ModelTracer(Base, __shared):
    __tablename__ = 'model_tracer'
    depth = Column(Numeric, primary_key=True)
    temperature = Column(Float, nullable=False)
