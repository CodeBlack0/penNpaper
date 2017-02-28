import re


class Descriptor:
    ''' Descriptor-baseclass '''
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance):
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Typed(Descriptor):
    ''' Typed descriptor-class '''
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError("Expected %s" % self.ty)
        super().__set__(instance, value)


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
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Must be >= 0')
        super().__set__(instance, value)


class Negative(Descriptor):
    ''' Descriptor for Negative Values '''
    def __set__(self, instance, value):
        if value > 0:
            raise ValueError('Must be <= 0')
        super().__set__(instance, value)


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
    def __set__(self, instance, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Expected as number')
        super().__set__(instance, float(value))


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

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance, value)


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

    def __set__(self, instance, value):
        if len(value) != self.size:
            raise ValueError('Not the correct size')


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

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError('Invalid string')
        super().__set__(instance, value)


class RegexString(String, Regex):
    ''' descriptor for string with a regex '''
    pass


class SizedRegexString(SizedString, Regex):
    ''' descriptor for string with a max size and a regex '''
    pass


class FixedSizedRegexString(FixedSizedString, Regex):
    ''' descriptor for string with a fixed size and a regex '''
    pass
