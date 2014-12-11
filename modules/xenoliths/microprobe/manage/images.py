"""
Imports probe images into the database.
"""

from ...application import app, db
from pathlib import Path

def import_images():
    basepath = Path(app.config.get("RAW_DATA"))/"Probe"/"images"
    import IPython; IPython.embed()
    
