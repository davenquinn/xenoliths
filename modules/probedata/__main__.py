from __future__ import division, print_function

from flask.ext.script import Manager, Server

from probedata.application import app, db
from probedata.management.setup import import_all
from probedata import models

manager = Manager(app)

server = Server(host='0.0.0.0', port=8000)
manager.add_command("serve", server)

@manager.shell
def make_context():
    return dict(app=app,db=db,models=models)

@manager.command
def setup(hard=False):
    with app.app_context():
        if hard: db.drop_all()
        db.create_all()
        import_all()


if __name__ == "__main__":
    manager.run()
