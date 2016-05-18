from data import summary_data
from json import dumps
from sys import stdout

_ = dumps(summary_data())
stdout.write(_)
