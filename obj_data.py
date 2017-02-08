import xml.etree.ElementTree as ElemTree
import os


########################################################################################################################
# Class for all static functions
class Data(object):
    # Parsing XML File
    def parse_file(path):
        try:
            if not isinstance(path, str):
                raise Exception('parse_file: path value not a string')
            if not os.path.isfile(path):
                raise Exception('parse_file: path not found')
            return ElemTree.parse(path).getroot()
        except Exception as ex:
            print(ex)

    parse_file = staticmethod(parse_file)

    # Parsed alle nodes im XML-Objekt in ein dictionary
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

    reparse_nodes = staticmethod(reparse_nodes)

    # Prints a raw datadict
    def print_dict(item):
        for k, data in item.items():
            print(str(k) + ': ' + str(data))

    print_dict = staticmethod(print_dict)

    # checks if string is numeric
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    is_number = staticmethod(is_number)
