class PersistentObject(object):
    def __init__(self, **kwargs):
        fields = super().__getattribute__('fields')

        d = {}
        for k in fields:
            if not k in kwargs:
                continue

            d[k] = kwargs[k]

        super().__setattr__('values', d)

    def __getattr__(self, name):
        if name not in super().__getattribute__('values'):
            raise AttributeError()

        return self.__getattribute__('values')[name]

    def __setattr__(self, name, value):
        if name not in self.__getattribute__('values'):
            raise AttributeError()

        self.__getattribute__('values')[name] = value

    def to_dict(self):
        return self.__getattribute__('values').copy()



def make_persistent_object(name, fields):
    def ctor(self, **kwargs):
        PersistentObject.__init__(self, **kwargs)

    return type(
        name,
        (PersistentObject, ),
        {
            'fields': tuple(fields),
            '__init__': ctor
        }
    )
