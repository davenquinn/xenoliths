from .base import Application
from ..database import db

app = Application(__name__)

db.init_app(app)

@app.route("/")
def root():
    return app.send_static_file('index.html')
