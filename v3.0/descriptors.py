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


class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Must be >= 0')
        super().__set__(instance, value)


class Negative(Descriptor):
    def __set__(self, instance, value):
        if value > 0:
            raise ValueError('Must be <= 0')
        super().__set__(instance, value)


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class Number(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Expected as number')
        super().__set__(instance, float(value))


class PositiveNumber(Number, Positive):
    pass


class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance, value)


class SizedString(String, Sized):
    pass


class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError('Invalid string')
        super().__set__(instance, value)


class RegexString(String, Regex):
    pass


class SizedRegexString(SizedString, Regex):
    pass
