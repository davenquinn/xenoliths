from uncertainties import ufloat, NegativeStdDev
from click import echo

def uval(u,s):
    return ufloat(u,abs(s))

class nested(object):
    """ Runs the wrapped function once for
        each child dict, adding a header based
        on its value.
    """
    def __init__(self, pre_func=None, nl=True):
        self.make_text = pre_func
        self.nl = nl

    def __call__(self, f):
        def wrapped_f(data):
            for k,v in list(data.items()):
                echo(self.make_text(k,v))
                f(v)
            if self.nl:
                echo("")
        return wrapped_f
