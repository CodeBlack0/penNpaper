from functools import wraps, partial
from xml.etree.ElementTree import parse
import sys
import imp
import os
import re

'''
Usage of the functionality implemented in this file:

debug: decotrator for debugging function/methodes
debugmethodes: decorator for debgging all the methodes in a class

_make_init: not to be used
MetaClass: is jsut a base metaclass for the implemented signature based definitions of classes

_xml_to_code: not to be used
_cls_to_class: not to be used
generate_custom_importer: generates a importer with a custom loader that applies to a given filetype
generate_custom_loader: generates a loader  which loads/imports the data from a given file with a given function/methode

install_XML_importer: installs a basic version of an xml-importer
--> <classes>
        <class name='Item'>
            <field type='PositiveInteger'>uuid</field>
            <field type='String'>name</field>
            <field type='PositiveNumber'>price</field>
            <field type='PositiveNumber'>weight</field>
            <field type='String'>special_text</field>
        </class>
    </classes>

    \/

    class Item(GameObject):
        uuid = des.PositiveInteger()
        name = des.String()
        price = des.PositiveNumber()
        weight = des.PositiveNumber()
        special_text = des.String()

'Descriptors': basically the data-types
'''

# DESCRIPTORS-----------------------------------------------------------------------------------------------


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

# METHODES/FUNCTIONS --------------------------------------------------------------------------------


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


def _xml_to_code(filename):
    ''' Parse class definitions from an xml file '''
    doc = parse(filename)
    code = '\nimport utility as util\n'
    for cls in doc.findall('class'):
        clscode = _cls_to_class(cls)
        code += clscode
    return code


def _cls_to_class(cls):
    ''' Parse a class out of a cls-node '''
    name = cls.get('name')
    code = 'class %s(util.BaseClass):\n' % name
    for field in cls.findall('field'):
        dtype = field.get('type')
        options = ['%s=%s' % (key, val) for key, val in field.items() if key != 'type']
        name = field.text.strip()
        code += '    %s = util.%s(%s)\n' % (name, dtype, ','.join(options))
    return code


def generate_custom_importer(loader, extension=None):
    class Importer:
        @classmethod
        def find_module(cls, fullname, path=None):
            for dirname in sys.path:
                filename = os.path.join(dirname, fullname + extension)
                if os.path.exists(filename):
                    return loader(filename)
            return None

    return Importer


def generate_custom_loader(func):
    class Loader:
        def __init__(self, filename):
            self.filename = filename

        def load_module(self, fullname):
            ''' make the module and carry out import '''
            if fullname in sys.modules:
                mod = sys.modules[fullname]
            else:
                mod = imp.new_module(fullname)
                sys.modules[fullname] = mod
            mod.__file__ = self.filename
            mod.__loader__ = self
            func(self, mod)
            return mod

    return Loader


XMLLoader = generate_custom_loader(lambda loader, mod: exec(_xml_to_code(loader.filename), mod.__dict__, mod.__dict__))
XMLImporter = generate_custom_importer(XMLLoader, '.xml')


def install_XML_importer():
    sys.meta_path.append(XMLImporter)
