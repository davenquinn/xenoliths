import click
import arrow

from flask.ext.migrate import MigrateCommand
from subprocess import call
from pathlib import Path

from ..application import app

def run(command):
    click.secho(command, fg="cyan")
    call(command, shell=True)

@MigrateCommand.command
def backup():
    """ Backs up database to PostgreSQL dump file"""
    click.echo("Backing up database...")
    db_name, data_dir = map(app.config.get,("DB_NAME","DATA_DIR"))

    fn = arrow.now().format('YYYY-MM-DD_HH.mm.ss')+".sql"
    path = Path(data_dir)/"backups"/fn
    run("pg_dump -Fc {0} > {1}".format(db_name, path))
    click.secho("Success!", fg="green")
