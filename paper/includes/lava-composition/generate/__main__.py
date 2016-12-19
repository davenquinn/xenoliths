#!/usr/bin/env python
#-*- coding: utf-8 -*-

from xenoliths.application import app
from xenoliths.models import ProbeMeasurement

from .table import describe

with app.app_context():
    from .query import queryset
    from .ternary import make_ternary
    from .figure import make_tas

    make_tas()
    make_ternary()

    print "Crystal Knob bulk composition"
    print "   estimated from defocused probe"
    print "   analysis (300µm spot size)"
    print "   n =", queryset.count()
    describe(queryset)
    print ""

    print "Olivine xenocryst composition"
    print "   (most depleted measurement)"
    print "   measurement id = 2359"
    describe(ProbeMeasurement.query.filter_by(id=2359))
    print ""

    print "Olivine phenocryst composition"
    print "   (most enriched measurement)"
    print "   measurement id = 2496"
    describe(ProbeMeasurement.query.filter_by(id=2496))
