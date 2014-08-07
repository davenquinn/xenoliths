from ..application import app, db

def start_over():
    with app.app_context():
        db.drop_all()
        db.create_all()
