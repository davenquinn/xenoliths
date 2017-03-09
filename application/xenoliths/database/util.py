import sqlalchemy.types as types

class Choice(object):
    def __init__(self,k,v):
        self.id = k
        self.name = v

    def __str__(self):
        return self.name

class ChoiceType(types.TypeDecorator):

    impl = types.String()

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value or k == value][0]

    def process_result_value(self, value, dialect):
        return Choice(value,self.choices[value])
