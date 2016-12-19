from os import path
from subprocess import Popen, PIPE, STDOUT
from xenoliths.microprobe.group import get_molar
from json import dumps

from ..query import queryset

def make_ternary():

    here = path.dirname(__file__)

    data = dict(
        molar=[get_molar(d)
                for d in queryset.all()],
        outfile="build/lava-composition.svg")

    p = Popen(['coffee', here],stdin=PIPE)
    p.communicate(input=dumps(data))
