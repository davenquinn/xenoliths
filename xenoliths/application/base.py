import logging
from os import path
from flask import Flask, Blueprint
from logging.handlers import RotatingFileHandler

from ..config import DATA_DIR, LOG_DIR

file_handler = RotatingFileHandler(
    path.join(LOG_DIR,"application.log"),
    backupCount=1, maxBytes=1e5)

_ = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(_)
file_handler.setLevel(logging.DEBUG)

data = Blueprint('static', __name__,
    static_folder=DATA_DIR,
    static_url_path="")

class Application(Flask):
    def __init__(self, *args,**kwargs):
        defaults = dict(
            static_url_path="static",
            static_folder="static")
        Flask.__init__(self, *args,**kwargs)
        self.config.from_object("xenoliths.config")
        self.register_blueprint(data, url_prefix="/data")
        self.logger.addHandler(file_handler)
