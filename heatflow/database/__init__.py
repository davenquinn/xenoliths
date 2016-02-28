from click import echo, secho, style
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import partial, wraps

from .models import meta
from ..config import DBNAME

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
