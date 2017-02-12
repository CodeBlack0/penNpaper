from obj_data import Data

data = Data('data_files.xml')
for wep_id, item in data.dependent['weapondata'].items():
    print('ID:', wep_id)
    for stat, value in data.dependent['itemdata'][wep_id].items():
        print(stat, '-->', value)
    for stat, value in item.items():
        print(stat, '-->', value)
