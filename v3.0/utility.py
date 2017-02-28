from functools import wraps, partial
from inspect import Parameter, Signature
from descriptors import Descriptor


def debug(func=None, *, prefix=''):
    ''' Functiondecorator for debugging code '''
    if func is None:
        return partial(debug, prefix=prefix)
    msg = prefix + func.__qualname__

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg + repr(args) + repr(kwargs))
        return func(*args, **kwargs)
    return wrapper


def debugmethodes(cls, *, prefix=''):
    ''' Applies debug-decorator to all methodes in class '''
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val, prefix=prefix))
    return cls


def make_signature(names):
    ''' Generates a signature object with given signature '''
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


class MetaClass(type):
    ''' MetaClass for GameObjects '''
    ''' Used in Python < 3.6, because in 3.6(+?) dictionaries are ordered by default
       @classmethod
       def __prepare__(cls, name, base):
            return OrderedDict()'''

    def __new__(cls, name, bases, clsdict):
        fields = [key for key, val in clsdict.items() if isinstance(val, Descriptor)]
        for name in fields:
            clsdict[name].name = name
        clsobj = super().__new__(cls, name, bases, dict(clsdict))
        sig = make_signature(fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj
