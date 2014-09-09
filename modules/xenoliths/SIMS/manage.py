from flask.ext.script import Manager
from ..application import app

SIMSCommand = Manager(usage="Command to manage SIMS data")
