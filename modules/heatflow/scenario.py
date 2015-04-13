class ModelScenario(object):
    def __init__(self, name, **kwargs):
        self.name = name
        for k,arg in kwargs.items():
            setattr(self,k,arg)

    def __call__(self):
        pass
