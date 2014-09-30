from flask.ext.script import Manager, Server

from .application import app, db
from .microprobe.manage.setup import import_all
from .database.manage import MigrateCommand
from .thermometry.command import TemperatureCommand
from .heatflow import HeatFlowCommand
from .SIMS import SIMSCommand
from . import models

manager = Manager(app)

server = Server(host='0.0.0.0', port=8000)
manager.add_command("serve", server)
manager.add_command("db", MigrateCommand)
manager.add_command("sims", SIMSCommand)
manager.add_command("temperature", TemperatureCommand)
manager.add_command("heat-flow", HeatFlowCommand)

@manager.command
def profile():
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run(debug = True, host='0.0.0.0', port=8000)


@manager.shell
def make_context():
    return dict(app=app,db=db,models=models)

@manager.command
def setup(hard=False):
    with app.app_context():
        db.create_all()
        import_all()
