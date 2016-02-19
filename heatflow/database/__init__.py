from click import secho
from sqlalchemy import create_engine

from ..config import DBNAME
from .models import meta, ModelRun, ModelTracer, ModelProfile

def connect_database():
    engine = create_engine(DBNAME)
    return engine.connect()

def create_tables():
    secho("Creating database tables", fg='green')
    conn = connect_database()
    conn.execute("CREATE SCHEMA "+meta.schema)
    meta.create_all(conn)
