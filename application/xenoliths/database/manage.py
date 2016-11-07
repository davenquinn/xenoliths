import click

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from psql_backup import PSQL_Backup

from ..application import app

config = (app.config.get("DB_NAME"),
        app.config.get("DB_BACKUP_DIR"))
commands = PSQL_Backup(*config)

MigrateCommand.command(commands.backup)
MigrateCommand.command(commands.restore)

@click.command()
def DBCommand():
    """ Command to manage database.
    """
    mgr = Manager(app)
    mgr.add_command("db", MigrateCommand)
    mgr.run()

# Hack for this command to play nice with click
DBCommand.allow_extra_args = True

