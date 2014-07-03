#!/usr/bin/env python

from __future__ import division, print_function

from flask.ext.script import Manager, Server

from samples.application import app, db

manager = Manager(app)

server = Server(host='0.0.0.0', port=8000)
manager.add_command("serve", server)

@manager.shell
def make_context():
	return dict(app=app,db=db)

if __name__ == "__main__":
    manager.run()
