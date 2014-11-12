from ...application import db
from sqlalchemy.orm import Session

class BaseModel(db.Model):
    __abstract__ = True
    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.query.filter_by(**kwargs).first()
        if obj is None:
            obj = cls(**kwargs)
        return obj

    @property
    def session(self):
        return Session.object_session(self)
