from flask.ext.migrate import Migrate

from .base import Application
from ..database import db

app = Application(__name__)

db.init_app(app)
migrate = Migrate(app, db)

from ..SIMS import sims
from ..thermometry import thermometry
app.register_blueprint(sims,url_prefix="/sims")
app.register_blueprint(thermometry,url_prefix="/temp")


@app.route("/")
def root():
    return app.send_static_file('index.html')
