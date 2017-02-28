from obj_data import Data
from obj_item import Item

data = Data('data_files.xml')
data.print_equipables()
print(Item({'name': 'test', 'price': 100.0, 'weight': 10.0, 'special_text': '', 'durability': 1}))
