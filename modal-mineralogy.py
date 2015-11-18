#!/usr/bin/env python

from __future__ import division

from os import path
from json import dumps
from subprocess import Popen, PIPE, STDOUT
from xenoliths import app
from xenoliths.models import Sample

here = path.dirname(__file__)

with app.app_context():
    data = {s.id: s.modes()
            for s in Sample.query
                .filter_by(xenolith=True)
                .all()}

script = path.join(here,"generate.coffee")

p = Popen(['coffee', script],stdin=PIPE)
p.communicate(input=dumps(data))
