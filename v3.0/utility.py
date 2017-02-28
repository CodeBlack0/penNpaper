from functools import wraps, partial
from descriptors import Descriptor


def debug(func=None, *, prefix=''):
    ''' Functiondecorator for debugging code '''
    if func is None:
        return partial(debug, prefix=prefix)
    msg = prefix + func.__qualname__

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper


def debugmethodes(cls=None, *, prefix=''):
    ''' Applies debug-decorator to all methodes in class '''
    if cls is None:
        return partial(debugmethodes, prefix=prefix)

    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val, prefix=prefix))
    return cls


def _make_init(fields):
    ''' Generates init code based on the given fields '''
    code = 'def __init__(self, %s):\n' % ','.join(fields)
    for name in fields:
        code += '   self.%s = %s\n' % (name, name)
    return code


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
        if fields:
            init_code = _make_init(fields)
            exec(init_code, globals(), clsdict)
        clsobj = super().__new__(cls, name, bases, dict(clsdict))
        return clsobj


class BaseClass(metaclass=MetaClass):
    ''' Standard base class '''
    pass
