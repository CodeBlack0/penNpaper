import os
import xml.etree.ElementTree as ElemTree
from obj_utility import Utility


class Parser(object):
    __slots__ = ['scales']

    # [UNIVERSAL PARSER] ===============================================================================================
    @staticmethod
    def parse(name, path):
        try:
            func = Parser.get_parse_function(name)
            return func(path)
        except Exception as err:
            print('parse(' + name + ', ' + path + ') generated: ', end='')
            print(err)

    @staticmethod
    def get_parse_function(name):
        try:
            # checking if there is a specific function for this file
            if ('parse_' + name) not in Parser.__dict__:
                # returning standardised function
                return Utility.curry(Parser.file_to_dict_by_attrib)(name=name.replace('data', ''), attribute='id',
                                                                    internalformat=None, keyformat=int)
            else:
                # returning specific function
                return Parser.__dict__['parse_' + name].__func__
        except Exception as err:
            print(err)

    # [SPECIFIC PARSERS] ===============================================================================================
    # parses the scales from scales.xml
    @staticmethod
    def parse_scales(path):
        try:
            # internal format of the scalenodes is parsed with this function
            def internalformat(x):
                return (Parser.elemtree_to_dict_by_attrib(x, attribute='symbol', name='unit',
                                                          internalformat=Utility.Helper.to_float),
                        x.attrib['synonyms'].split(', '))

            # parsing data
            scales = Parser.file_to_dict_by_attrib(path=path, attribute='label', name='scale', keyformat=str,
                                                   internalformat=internalformat)
            # remember scales
            Parser.scales = scales
            return scales
        except Exception as err:
            print(err)

    # parses the spelldata from spelldata.xml
    @staticmethod
    def parse_spelldata(path):
        try:
            # internal format of the spellnodes is parsed with this function
            internalformat = (Utility.curry(Parser.elemtree_to_dict_by_name)
                              (keyformat=None, internalformat=Utility.Helper.to_float))
            # parsing data
            return Parser.file_to_dict_by_attrib(path=path, attribute='id', name='spell', keyformat=int,
                                                 internalformat=internalformat)
        except Exception as err:
            print(err)

    # parses the itemdata from an itemdata.xml
    @staticmethod
    def parse_itemdata(path):
        try:
            # internal format of the itemnodes is parsed with this function
            internalformat = (Utility.curry(Parser.elemtree_to_dict_by_name)
                              (keyformat=None, internalformat=Utility.Helper.to_float))

            # parsing data
            return Parser.file_to_dict_by_attrib(path=path, attribute='id', name='item', keyformat=int,
                                                 internalformat=internalformat)
        except Exception as err:
            print(err)

    # parses the itemdata from an itemdata.xml
    @staticmethod
    def parse_weapondata(path):
        try:
            # internal format of the weaponnodes is parsed with this function
            def internalformat(x):
                return {'hands': Utility.Helper.to_int(x),
                        'equiptime': Utility.Helper.to_scale(x, scales=Parser.scales),
                        'attacks': Parser.elemtree_to_dict_by_attrib(x, name='attack', attribute='id', keyformat=int,
                                                                     internalformat=Parser.parse_attack),
                        'upgradepath': Parser.parse_upgradepath(x)}[x.tag]

            # parsing data
            return Parser.file_to_dict_by_attrib(path=path, attribute='id', name='weapon', keyformat=int,
                                                 internalformat=(Utility.curry(Parser.elemtree_to_dict_by_name))
                                                 (keyformat=None, internalformat=internalformat))
        except Exception as err:
            print(err)

    # parses the attackdata from a given ElementTree
    @staticmethod
    def parse_attack(elemtree):
        try:
            def internalformat(x):
                return {'range': Utility.Helper.to_scale(x, scales=Parser.scales),
                        'executiontime': Utility.Helper.to_scale(x, scales=Parser.scales),
                        'crit': Parser.elemtree_to_dict_by_name(x, internalformat=Utility.Helper.text),
                        'damage': Parser.elemtree_to_dict_by_name(x, internalformat=Utility.Helper.text),
                        'type': Utility.Helper.text(x)}[x.tag]

            return Parser.elemtree_to_dict_by_name(elemtree, internalformat=internalformat)
        except Exception as err:
            print(err)

    # parses the upgradepathdata from a given ElementTree
    @staticmethod
    def parse_upgradepath(elemtree):
        try:
            return elemtree
        except Exception as err:
            print(err)

    # ==[BASIC PARSING FUNCTIONS]=======================================================================================
    '''
    Parser Formats:
  ----------------------------------------
    Parsers take a Elementtree(elemtree)/filepath(path) and read the data from it either by a given ATTRIBUTE
    or the NAME of the tags in question into a DICTIONARY. They can also take a KEYFORMAT and aply it to the KEYS
    of the DICTIONARY and an INTERNALFORMAT and aply it to the INTERNALDATA of the DICTIONARY.

    Intendend Usage:
  ----------------------------------------
    For Example:
    <items>
        <item id=4>
            <name>Beer</name>
            <price>1</price>
            <weight>500</weight>
        </item>
    </items>
    Is parsed with this function:
    items = Utility.file_to_dict_by_attrib(path=path, attribute='id', name='item', keyformat=int,
                                           internalformat=(Utility.curry(Utility.elemtree_to_dict_by_name)
                                                             (keyformat=None, internalformat=Utility.Helper.to_float)))
        --> 'file_to_dict_by_attrib' takes PATH, ATTRIBUTE, NAME, KEYFORMAT, and INTERNALFORMAT and
            parses the first layer (<item id='4'>...</item> --> {4: ...}. The INTERNALDATA (...) of this is another
            'elemtree' and the function aplies the given INTERNALFORMAT to it, which results in it being also parsed
            into a dict. (Here the INTERNALFORMAT must be curried, because we want 'prime' it with certain arguments
            before its execution, because we can't give it these arguments at runtime)
    '''

    # [PARSE FILE --> ElemTree]
    # parse a xmlfile to the xml-api's elemtree-object
    @staticmethod
    def xml_to_elemtree(path):
        try:
            if not isinstance(path, str):
                raise Exception('parse_file: path value not a string, is: '
                                + str(type(path)) + ' --> ' + str(path))
            if not os.path.isfile(path):
                raise Exception('parse_file: path not found')
            return ElemTree.parse(path).getroot()
        except Exception as err:
            print(err)

    # [PARSE ElemTree --> {tag: text | (tag, text) <-- ElemTree}
    # parse an elemtree-object to a dict by node-names as keys
    @staticmethod
    def elemtree_to_dict_by_name(elemtree, internalformat=None, keyformat=None):
        try:
            # check if elemtree is of type ElemTree
            if not isinstance(elemtree, ElemTree.Element):
                raise Exception('parse_elemtree_to_dict_by_name: elemtree value not a ElementTree, is: '
                                + str(type(elemtree)) + ' --> ' + str(elemtree))

            # setting formats if not set through parameters (standard format is identity function)
            keyformat = Utility.Helper.identity if keyformat is None else keyformat
            internalformat = Utility.Helper.identity if internalformat is None else internalformat

            # parsing elemtree to dict and reformating data with given functions
            return {keyformat(x.tag): internalformat(x) for x in elemtree}
        except Exception as err:
            print(err)

    # [PARSE FILE --> ElemTree --> {tag: text | (tag, text) <-- ElemTree}
    # parses a xmlfile to a dict with 'parse_elemtree_to_dict_by_name'
    @staticmethod
    def file_to_dict_by_name(path, internalformat=None, keyformat=None):
        try:
            # file to elemtree
            elemtree = Parser.xml_to_elemtree(path)

            # elemtree to dict by name
            return Parser.elemtree_to_dict_by_name(elemtree, internalformat=internalformat, keyformat=keyformat)
        except Exception as err:
            print(err)

    # [PARSE ElemTree --> {attrib_val: text | (attrib_val, text) <-- ElemTree}
    # parse an elemtree to dict using certain attributes as keys
    @staticmethod
    def elemtree_to_dict_by_attrib(elemtree, attribute, internalformat=None, keyformat=None, name=None):
        try:
            # check if elemtree is of type ElemTree
            if not isinstance(elemtree, ElemTree.Element):
                raise Exception('parse_elemtree_to_dict_by_attribute: elemtree value not a ElementTree, is: '
                                + str(type(elemtree)) + ' --> ' + str(elemtree))

            # setting formats if not set through parameters (standard format is identity function)
            keyformat = Utility.Helper.identity if keyformat is None else keyformat
            internalformat = Utility.Helper.identity if internalformat is None else internalformat

            # check if tag was given to parse by (if so setting elemtree to tag-specific iter-object)
            if name is not None:
                elemtree = elemtree.iter(name)

            # parsing elemtree to dict and reformating data with given functions
            return {keyformat(x.attrib[attribute]): internalformat(x) for x in elemtree}
        except Exception as err:
            print(err)

    # [PARSE File --> ElemTree --> {attrib_val: text | (attrib_val, text) <-- ElemTree}
    # parses a xmlfile to a dict with 'parse_elemtree_to_dict_by_attribute'
    @staticmethod
    def file_to_dict_by_attrib(path, attribute, internalformat=None, keyformat=None, name=None):
        try:
            # file to elemtree
            elemtree = Parser.xml_to_elemtree(path)

            # elemtree to dict by attribute
            return Parser.elemtree_to_dict_by_attrib(elemtree, attribute, name=name, keyformat=keyformat,
                                                     internalformat=internalformat)
        except Exception as err:
            print(err)
