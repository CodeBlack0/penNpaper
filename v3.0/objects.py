from utility import MetaClass
import descriptors as des
import inspect


class GameObject(metaclass=MetaClass):
    ''' Baseclass for GameObjects '''
    _fields = []

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)


class Item(GameObject):
    uuid = des.PositiveInteger()
    name = des.String()
    price = des.PositiveNumber()
    weight = des.PositiveNumber()
    special_text = des.String()


item = Item(0, 'test', weight=7, special_text='testing', price=1)

print(inspect.signature(Item))
print(item.__dict__)
