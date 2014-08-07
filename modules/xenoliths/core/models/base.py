from ...application import db

class BaseModel(db.Model):
    __abstract__ = True
    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.query.filter_by(**kwargs).first()
        if obj is None:
            obj = cls(**kwargs)
        return obj
