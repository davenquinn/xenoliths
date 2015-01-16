import os

DATA_DIR = os.environ["DATA_DIR"]

def results_dir(file=None):
    return os.path.join(DATA_DIR,"results","heat-flow",file)

