import re
from datetime import datetime

from ...application import db

date_regex = re.compile(r"(\d\d-\d\d-\d\d)")

def model_factory(cls, echo=False):
    """
    Factory function that returns a method
    to get or create a database model, as appropriate.

    Arguments:
      cls    A database model class
      echo   Whether to print on new model creation (default False)
    """
    def get_or_create(**kwargs):
        obj = cls.query.filter_by(**kwargs).first()
        if obj is None:
            obj = cls(**kwargs)
            if echo:
                print("Created new "+cls.__name__+": "+repr(obj))
            db.session.add(obj)
        return obj

    return get_or_create

def find_date(string):
    """
    Finds a date formatted in the MM-DD-YY scheme
    in the given string, and returns a corresponding
    datetime object. Helps find the dates that measurements
    were taken.
    """
    date = date_regex.search(string).group()
    return datetime.strptime(date, "%m-%d-%y")
