from flask.ext.sqlalchemy import SQLAlchemy

from .base import Application

db = SQLAlchemy()
app = Application(__name__)

db.init_app(app)

@app.route("/")
def root():
    return app.send_static_file('index.html')
