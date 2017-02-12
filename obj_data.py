from obj_utility import Utility
from obj_parser import Parser


# from obj_item import Item, Upgradeable, Weapon, Equipment


class Data(object):
    __slots__ = ['independent', 'dependent']

    def __init__(self, path=None):
        if path is None:
            path = 'data_files.xml'
        self.independent, self.dependent = dict(), dict()

        # parsing 'data_files.xml' into a dict
        files = Parser.file_to_dict_by_name(path, internalformat=(Utility.curry(Parser.elemtree_to_dict_by_attrib)
                                                                  (attribute='name', name='file', keyformat=None,
                                                                   internalformat=Utility.Helper.text)))

        # parsing base independent data
        for name, file in files['independent'].items():
            self.independent[name] = Parser.parse(name, file)

        # parsing dependent data
        for name, file in files['dependent'].items():
            self.dependent[name] = Parser.parse(name, file)
