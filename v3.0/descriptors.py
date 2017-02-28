import re


def _make_setter(dcls):
    ''' Generates code for the setter function of a descriptor '''
    code = 'def __set__(self, instance, value):\n'
    for d in dcls.__mro__:
        if 'set_code' in d.__dict__:
            for line in d.set_code():
                code += '    ' + line + '\n'
    return code


class DescriptorMeta(type):
    ''' Metaclass for descriptors '''
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        if '__set__' in clsdict:
            raise TypeError('use set_code(), not __set__()')
        code = _make_setter(self)
        exec(code, globals(), clsdict)
        setattr(self, '__set__', clsdict['__set__'])


class Descriptor(metaclass=DescriptorMeta):
    ''' Descriptor-baseclass '''
    def __init__(self, name=None):
        self.name = name

    @staticmethod
    def set_code():
        return ['instance.__dict__[self.name] = value']

    def __get__(self, instance):
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Typed(Descriptor):
    ''' Typed descriptor-class '''
    ty = object

    @staticmethod
    def set_code():
        return ['if not isinstance(value, self.ty):',
                '    raise TypeError("Expected %s" % self.ty)']


class Integer(Typed):
    ''' Typed-descriptor for integers '''
    ty = int


class Float(Typed):
    ''' Typed-descriptor for floats '''
    ty = float


class List(Typed):
    ''' Typed-descriptor for lists '''
    ty = list


class Dict(Typed):
    ''' Typed-descriptor for dictionaries '''
    ty = dict


class String(Typed):
    ''' Typed-descriptor for strings '''
    ty = str


class Positive(Descriptor):
    ''' Descriptor for Positive Values '''
    @staticmethod
    def set_code():
        return ['if value < 0:',
                '    raise ValueError("Must be >= 0")']


class Negative(Descriptor):
    ''' Descriptor for Negative Values '''
    @staticmethod
    def set_code():
        return ['if value > 0:',
                '    raise ValueError("Must be <= 0")']


class PositiveInteger(Integer, Positive):
    ''' descriptor for postive integers'''
    pass


class PositiveFloat(Float, Positive):
    ''' descriptor for postive floats'''
    pass


class NegativeInteger(Integer, Negative):
    ''' descriptor for negative integers'''
    pass


class NegativeFloat(Float, Negative):
    ''' descriptor for negative floats'''
    pass


class Number(Descriptor):
    ''' descriptor for numbers (i.e. integers and floats) '''
    @staticmethod
    def set_code():
        return ['if not isinstance(value, int) and not isinstance(value, float):',
                '    raise TypeError("Expected as number")']


class PositiveNumber(Number, Positive):
    ''' descriptor for positive numbers'''
    pass


class NegativeNumber(Number, Negative):
    ''' descriptor for negative numbers'''
    pass


class Sized(Descriptor):
    ''' descriptor for values with a given size '''
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_code():
        return ['if len(value) > self.maxlen:',
                '    raise ValueError("Too big")']


class SizedString(String, Sized):
    ''' descriptor for strings with a max size '''
    pass


class SizedList(List, Sized):
    ''' descriptor for lists with a max size '''
    pass


class SizedDict(Dict, Sized):
    ''' descriptor for dicts with a max size '''
    pass


class FixedSized(Descriptor):
    ''' descriptor for values with a fixed size '''
    def __init__(self, *args, size, **kwargs):
        self.size = size
        super().__init__(*args, **kwargs)

    def set_code():
        return ['if len(value) != self.maxlen:',
                '    raise ValueError("Not proper size")']


class FixedSizedString(String, FixedSized):
    ''' descriptor for string with a fixed size '''
    pass


class FixedSizedList(List, FixedSized):
    ''' descriptor for lists with a fixed size '''
    pass


class FixedSizedDict(Dict, FixedSized):
    ''' descriptor for dicts with a fixed size '''
    pass


class Regex(Descriptor):
    ''' descriptor for regex-able terms '''
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def set_code():
        return ['if not self.pat.match(value):',
                '    raise ValueError("Invalid string")']


class RegexString(String, Regex):
    ''' descriptor for string with a regex '''
    pass


class SizedRegexString(SizedString, Regex):
    ''' descriptor for string with a max size and a regex '''
    pass


class FixedSizedRegexString(FixedSizedString, Regex):
    ''' descriptor for string with a fixed size and a regex '''
    pass
