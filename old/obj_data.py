import xml.etree.ElementTree as ElemTree
import os
import functools


########################################################################################################################
# Class for all static functions
class Data(object):
    # Parsing XML File
    @staticmethod
    def parse_file(path):
        try:
            if not isinstance(path, str):
                raise Exception('parse_file: path value not a string')
            if not os.path.isfile(path):
                raise Exception('parse_file: path not found')
            return ElemTree.parse(path).getroot()
        except Exception as ex:
            print(ex)

    # Parsed alle nodes im XML-Objekt in ein dictionary
    @staticmethod
    def reparse_nodes(root):
        try:
            if not isinstance(root, ElemTree.Element):
                raise Exception(
                    'reparse_nodes: root is not a xml.etree.ElementTree.Element, root is ' + str(type(root)))
            raw_data = dict()
            for i, child in enumerate(root):
                raw_data[child.tag] = root[i]
            return raw_data
        except Exception as ex:
            print(ex)

    # Prints a raw datadict
    @staticmethod
    def print_dict(item):
        for k, data in item.items():
            print(str(k) + ': ' + str(data))

    # checks if string is numeric
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
