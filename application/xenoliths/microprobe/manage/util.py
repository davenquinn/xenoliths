import re
from datetime import datetime

from ...application import db

date_regex = re.compile(r"(\d\d-\d\d-\d\d)")

def model_factory(cls, echo=False, flush=True):
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
                print(("Created new "+cls.__name__+": "+repr(obj)))
            db.session.add(obj)
            if flush:
                db.session.flush()
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

size_field = re.compile(r"defocused_(\d+)um")
digit_regex = re.compile(r"(\d+)")

def find_spot_size(string):
    """
    Finds the size of the probe spot used in a measurement
    given a sample name containing a string such as
    `defocused_xxx_um`
    """
    s = size_field.search(string)
    if s == None:
        return 0
    else:
        m = digit_regex.search(s.group())
        return int(m.group())
