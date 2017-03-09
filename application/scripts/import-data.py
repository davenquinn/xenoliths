#!/usr/bin/env python
"""
Script to transition tag and classification data to new database (Flask project) from old database (Django project).
"""
from sqlalchemy import MetaData, Table, create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import create_session, load_only, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from xenoliths.models import Sample,Point
from xenoliths.application import app, db
from xenoliths.microprobe.manage.setup import write_json

OLD_DATABASE = "xenoliths"

#Create and engine and get the metadata
Base = declarative_base()
engine = create_engine('postgresql://localhost/{0}'.format(OLD_DATABASE))
metadata = MetaData(bind=engine)

def table(name,*args,**kwargs):
    """An autoloading table based on the engine above"""
    kwargs["autoload"] = True
    return Table(name, metadata, *args, **kwargs)


class Tag(Base):
    __table__ = table('taggit_tag')

fkcol = Column('object_id', Integer, ForeignKey('samples_point.id'))
tags_table = table('taggit_taggeditem',fkcol)

class DjangoPoint(Base):
    __table__ = table('samples_point')
    tags = relationship('Tag', secondary=tags_table)

class DjangoSample(Base):
    __table__ = table('samples_sample')

session = create_session(bind=engine)

# Updates sample ID by changing shortened form
update_id = lambda s: s.replace("CKD","CK-D")

def import_tags():
    for old in session.query(DjangoPoint).all():
        res = Point.query.filter_by(
            sample_id=update_id(old.sample_id),
            line_number=old.n).all()
        if len(res) == 0: continue
        assert len(res) == 1
        new = res[0]

        slugs = [tag.slug for tag in old.tags]
        print(",".join(slugs))
        list(map(new.add_tag, slugs))
        db.session.commit()

    write_json()

def import_classification():
    import numpy as N
    from pickle import loads
    from base64 import b64decode
    from zlib import decompress

    for old in session.query(DjangoSample).all():
        new = Sample.query.get(update_id(old.id))
        print(new)
        cls = loads(decompress(b64decode(old.classification)))
        if not cls: continue
        shape = list(map(int,(cls['h'],cls['w'])))
        arr = N.array([i["v"] for i in cls.pop("values")])
        new.classification = arr.reshape(shape).tolist()
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        import_tags()
        import_classification()
