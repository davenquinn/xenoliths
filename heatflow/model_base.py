from click import echo
from .database import db, Recorder

class ModelRunner(object):
    def __init__(self, **info):
        self.info = info

    def run(self):
        pass

    def __call__(self, *args, **kwargs):
        self.recorder = Recorder(db, name=self.name)
        self.record = self.recorder
        try:
            self.run(*args,**kwargs)
        except Exception as err:
            echo("Rolling back session")
            self.recorder.session.rollback()
        finally:
            self.recorder.session.commit()
