from __future__ import division, print_function

from flask.ext.script import Manager, Server

from xenoliths.application import app, db
from xenoliths.microprobe.manage.setup import import_all
from xenoliths.microprobe import models
from xenoliths.database.manage import MigrateCommand
from xenoliths.thermometry.command import TemperatureCommand
from xenoliths.heatflow import HeatFlowCommand

manager = Manager(app)

server = Server(host='0.0.0.0', port=8000)
manager.add_command("serve", server)
manager.add_command("db", MigrateCommand)

manager.add_command("temperature", TemperatureCommand)
manager.add_command("heat-flow", HeatFlowCommand)

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
