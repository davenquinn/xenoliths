#!/usr/bin/env python

from __future__ import division, print_function

from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand

from samples.app import app
from samples.database import db, models

manager = Manager(app)

server = Server(host='0.0.0.0', port=8000)
manager.add_command("serve", server)
manager.add_command("database", MigrateCommand)

@manager.shell
def make_context():
	return dict(app=app,db=db,models=models)

if __name__ == "__main__":
    manager.run()
