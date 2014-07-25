from __future__ import print_function

from flask import Flask, Blueprint
from ..config import DATA_DIR

data = Blueprint('static', __name__,
    static_folder=DATA_DIR,
    static_url_path="")

class Application(Flask):
    def __init__(self, *args,**kwargs):
        defaults = dict(
            static_url_path="static",
            static_folder="static")
        Flask.__init__(self, *args,**kwargs)
        self.config.from_object("samples.config")
        self.register_blueprint(data, url_prefix="/data")
