from copy import copy

from obj_game import Game
from obj_item import Item, Weapon, Equipment, Upgradeable
from old.obj_data import Data


########################################################################################################################
# Class for managment of player data
class Player(object):
    # dict all Player-instances
    instances = dict()
    __slots__ = ['uuid', 'data', 'inventory', 'parent']

    def __init__(self, path=None, parent=None):
        self.uuid = id(self)
        Player.instances[self.uuid] = self
        self.data = dict()
        self.data['inventory'] = {
            "bag": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None},
            "weapons": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None},
            "equipments": {1: None, 2: None, 3: None, 4: None},
            "weight": 0}
        self.parent = parent if parent is not None else Game.general
        try:
            raw_data = Data.parse_file(path)
            data = Data.reparse_nodes(raw_data)
            self.parse_stats(data['stats'])
            self.parse_inventory(data['inventory'])
        except Exception as err:
            print("Failed to initialize Player from " + str(path) + ", because: \n" + err)

    # Parsing data =====================================================================================================
    # Parsing player stats ===============================================
    def parse_stats(self, raw_data):
        stats = dict()
        for child in raw_data[0]:
            stats[child.tag] = child.text

        stats['rolled'] = dict()
        for child in raw_data[1][0]:
            stats['rolled'][child.tag] = int(child.text)

        stats['string'] = dict()
        for child in raw_data[1][1]:
            stats['string'][child.tag] = int(child.text)

        self.data['stats'] = stats

    # Parsing players inventory ==========================================
    def parse_inventory(self, raw_data):
        try:
            data = Data.reparse_nodes(raw_data)
            self.parse_bag(data['bag'])
            self.parse_weapons(data['weapons'])
            self.parse_equipments(data['equipments'])
        except Exception as err:
            print(err)

    # parsing bag ========================================================
    def parse_bag(self, raw_data):
        for child in raw_data:
            if child.tag == "item":
                self.parse_item(child)
            elif child.tag == "weapon":
                self.parse_weapon(child)
            elif child.tag == "equipment":
                self.parse_equipment(child)

    def parse_item(self, data):
        item = self.parent.item(int(data.attrib['itemid']))
        item.set_specific_save_data(data)
        self.add_item_to_inventory(item)

    # parsing weapons ====================================================
    def parse_weapons(self, raw_data):
        for child in raw_data:
            self.parse_weapon(child, equip=True)

    def parse_weapon(self, data, equip=False):
        weapon = self.parent.weapon(int(data.attrib['itemid']), size=data.attrib['size'])
        weapon.set_specific_save_data(data)
        if equip:
            self.equip_item(weapon)
        else:
            self.add_item_to_inventory(weapon.uuid)

    # parsing equipments =================================================
    def parse_equipments(self, raw_data):
        for child in raw_data:
            self.parse_equipment(child, equip=True)

    def parse_equipment(self, data, equip=False):
        equipment = self.parent.equipment(int(data.attrib['itemid']))
        equipment.set_specific_save_data(data)
        if equip:
            self.equip_item(equipment)
        else:
            self.add_item_to_inventory(equipment.uuid)

    # Inventory Managment ==============================================================================================
    # adds a given [items uuid/item uuid] to the inventory ===============
    def add_item_to_inventory(self, item, position='bag', index=None):
        # getting uuid
        if isinstance(item, Item):
            uuid = item.uuid
        elif item in Item.instances:
            uuid = item
        elif item is not None:
            return False
        # swap item with certian slot
        if index is not None and index in self.data['inventory'][position]:
            temp, self.data['inventory'][position][index] = \
                self.data['inventory'][position][index], uuid
            return temp if temp is not None else True
        # regular insert into inventory
        else:
            for k, v in self.data['inventory'][position].items():
                if v is None:
                    self.data['inventory'][position][k] = uuid
                    return k
        return False

    # removes a given index from the inventory and returns it ============
    def remove_item_from_inventory(self, index):
        if index not in self.inventory['bag']:
            return False
        return self.add_item_to_inventory(None, position='bag', index=index)

    # equips a give [items uuid/item uuid] into the correct slot =========
    def equip_item(self, uuid, index=None):
        if isinstance(uuid, Item):
            uuid = uuid.uuid
        elif uuid not in Item.instances:
            return False
        if isinstance(Item.instances[uuid], Weapon):
            return self.add_item_to_inventory(uuid, position='weapons', index=index)
        if isinstance(Item.instances[uuid], Equipment):
            return self.add_item_to_inventory(uuid, position='equipments', index=index)
        else:
            return False

    # equips an item from the inventory based on a given index ===========
    def equip_from_inventory(self, index):
        if isinstance(self.inventory['bag'][index], Upgradeable):
            return self.equip_item(self.remove_item_from_inventory(index))
        else:
            return False

    # Debugging ========================================================================================================
    # Print player inventory =============================================
    def print_inventory(self, full=False):
        print('----[Player Inventory][Player UUID: ' + str(self.uuid) + ']---- \n<-- [Bag] -->')
        for k, item in self.inventory['bag'].items():
            self.print_inventory_slot(k, item, full)
        print('<-- [Weapons] -->')
        for k, weapon in self.inventory['weapons'].items():
            self.print_inventory_slot(k, weapon, full)
        print('<-- [Equipment] -->')
        for k, equipment in self.inventory['equipments'].items():
            self.print_inventory_slot(k, equipment, full)

    # prints a single slot with given values =============================
    @staticmethod
    def print_inventory_slot(k, item, full=True):
        print('[Slot ' + str(k) + '] | ', end='')
        if item is None:
            print('--empty--')
        elif isinstance(item, Item):
            if full:
                print()
                item.print_data()
            else:
                print(item.data['name'] + " [" + item.data['special_text'] + "]")

        else:
            print('--illegal item--')

    # prints player data =================================================
    def print_data_dict(self):
        for k in self.data:
            print(k + ": " + str(self.data[k]))

    # generates a new and independent memory location for the data-dict ==
    def realloc_mem_location(self):
            while id(self.data) in Item.data_addresses:
                self.data = copy(self.data)
            Item.data_addresses.append(id(self.data))
