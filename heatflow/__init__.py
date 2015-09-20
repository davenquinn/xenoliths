import os

DATA_DIR = os.environ["DATA_DIR"]

def results_dir(*args):
    d = os.path.join(DATA_DIR,"results","heat-flow")
    if len(args) > 0:
        return os.path.join(d,*args)
    else:
        return d

