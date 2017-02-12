from obj_data import Data
from obj_parser import Parser

data = Data('data_files.xml')
for id, item in data.dependent['weapondata'].items():
    print('ID:',id)
    for stat, value in data.dependent['itemdata'][id].items():
        print(stat, '-->', value)
    for stat, value in item.items():
        print(stat, '-->', value)
