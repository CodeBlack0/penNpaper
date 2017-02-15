class Item(dict):

    # standard definition of an item con´tians these datapoint with the given data types (are given as example)
    legal_attributes = {'name': '', 'price': .0, 'weight': .0, 'special_text': '', 'durability': 1}

    def __init__(self, arg, legal_attrib=None):
        try:
            # check if attribute-statndard is given if not get it from class
            if legal_attrib is None:
                legal_attrib = type(self).legal_attributes

            # check if given argument is a dict
            if not isinstance(arg, dict):
                raise Exception('Item.__init__: argument must be of type dict')

            # check if the given argument contains the right amount of elements
            if not len(arg) == len(legal_attrib):
                raise Exception('Item.__init__: argument does not have all the needed attributes')

            # check if each element...
            for attribute, value in arg.items():
                # ...is supposed to exist
                if attribute not in legal_attrib:
                    raise Exception('Item.__init__: illegal attribute --> ' + str(attribute))
                # ...has the right data type
                if not isinstance(value, type(legal_attrib[attribute])):
                    raise Exception('Item.__init__: illegal data type --> ' + str(attribute) + ':' + str(arg[attribute]) +
                                    ' should be ' + str(type(type(self).legal_attributes.legal_attributes[attribute])))
        except Exception as err:
            print(err)
        else:
            # if all is good pass the argument on
            super(Item, self).__init__(arg)
