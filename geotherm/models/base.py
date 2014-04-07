from __future__ import division
import numpy as N

class BaseModel(object):
    defaults = {}
    def __init__(self,**kwargs):
        for key,item in self.defaults.items():
            i = kwargs.pop(key,item)
            setattr(self, key, i)
