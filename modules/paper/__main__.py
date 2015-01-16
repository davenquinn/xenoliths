#! python

from paper.cli import cli
from paper.util import cd
from xenoliths.application import app

with app.app_context():
    d = app.config.get("SITE_DIR")+"/paper"
    with cd(d):
        cli()
