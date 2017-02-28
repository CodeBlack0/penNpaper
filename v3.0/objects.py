from utility import BaseClass, debugmethodes
import descriptors as des
import inspect


class GameObject(BaseClass):
    ''' Baseclass for gameobjects '''
    pass


@debugmethodes
class Item(GameObject):
    uuid = des.PositiveInteger()
    name = des.String()
    price = des.PositiveNumber()
    weight = des.PositiveNumber()
    special_text = des.String()


item = Item(0, 'test', weight=7, special_text='testing', price=1)

print(inspect.signature(Item))
print(item.__dict__)
