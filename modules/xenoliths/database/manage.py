from flask.ext.script import Manager
from subprocess import call
from pathlib import Path

from ..application import app

MigrateCommand = Manager()

@MigrateCommand.command
def backup():
    db_name, data_dir = map(app.config.get,("DB_NAME","DATA_DIR"))

    import IPython; IPython.embed()
