from functools import wraps
from inspect import signature

def uses(*dependencies):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            fkwargs = kwargs.copy()
            for d in dependencies:
                name = d.__name__
                value = d()

                fkwargs[name] = value

            return f(*args, **fkwargs)
            
        return wrapper

    return decorator

def instance(name, obj):
    result = lambda: obj
    result.__name__ = name

    return result

def transient(name, factory):
    result = lambda: factory()
    result.__name__ = name

    return result