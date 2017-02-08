from obj_data import Data
from obj_item import Item, Weapon, Equipment, Upgradeable
from obj_game import Game


########################################################################################################################
# Class for managment of player data
class Player(object):
    # dict all Player-instances
    instances = dict()

    def __init__(self, path=None, parent=None):
        self.uuid = id(self)
        Player.instances[self.uuid] = self
        self.data = dict()
        self.inventory = {
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
        except OSError as err:
            print("Failed to initialize Player from " + str(path))
            print(err)

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
        data = Data.reparse_nodes(raw_data)
        self.parse_bag(data['bag'])
        self.parse_weapons(data['weapons'])
        self.parse_equipments(data['equipments'])

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
        item = self.parent.item(int(data.attrib['itemid']), save_data=data)
        self.add_item_to_inventory(item)

    # parsing weapons ====================================================
    def parse_weapons(self, raw_data):
        for child in raw_data:
            self.parse_weapon(child, equip=True)

    def parse_weapon(self, data, equip=False):
        weapon = self.parent.weapon(int(data.attrib['itemid']), save_data=data)
        if equip:
            self.equip_item(weapon)
        else:
            self.add_item_to_inventory(weapon.uuid)

    # parsing equipments =================================================
    def parse_equipments(self, raw_data):
        for child in raw_data:
            self.parse_equipment(child, equip=True)

    def parse_equipment(self, data, equip=False):
        equipment = self.parent.equipment(int(data.attrib['itemid']), save_data=data)
        if equip:
            self.equip_item(equipment)
        else:
            self.add_item_to_inventory(equipment.uuid)

    # Inventory Managment ==============================================================================================
    # adds a given [items uuid/item uuid] to the inventory ===============
    def add_item_to_inventory(self, item, slot='bag'):
        if isinstance(item, Item):
            uuid = item.uuid
        elif item in Item.instances:
            uuid = item
        else:
            return False
        for k, v in self.inventory[slot].items():
            if v is None:
                self.inventory[slot][k] = uuid
                return k
        return False

    # removes a given index from the inventory and returns it ============
    def remove_item_from_inventory(self, index, swap=None):
        if index not in self.inventory['bag']:
            return False
        temp, self.inventory['bag'][index] = self.inventory['bag'][index], swap
        return temp

    # equips a give [items uuid/item uuid] into the correct slot =========
    def equip_item(self, uuid):
        if isinstance(uuid, Item):
            uuid = uuid.uuid
        elif uuid not in Item.instances:
            return False
        if isinstance(Item.instances[uuid], Weapon):
            return self.add_item_to_inventory(uuid, slot='weapons')
        if isinstance(Item.instances[uuid], Equipment):
            return self.add_item_to_inventory(uuid, slot='equipments')
        else:
            return False

    # equips an item from the inventory based on a given index ===========
    def equip_from_inventory(self, index):
        if isinstance(Item.instances[self.inventory['bag'][index]], Upgradeable):
            return self.equip_item(self.remove_item_from_inventory(index))
        else:
            return False

    # Debugging ========================================================================================================
    # Print player inventory =============================================
    def print_inventory(self, full=False):
        print('----[Player Inventory][Player UUID: ' + str(self.uuid) + ']---- \n<-- [Bag] -->')
        for k, uuid in self.inventory['bag'].items():
            self.print_inventory_slot(k, uuid, full)
        print('<-- [Weapons] -->')
        for k, uuid in self.inventory['weapons'].items():
            self.print_inventory_slot(k, uuid, full)
        print('<-- [Equipment] -->')
        for k, uuid in self.inventory['equipments'].items():
            self.print_inventory_slot(k, uuid, full)

    # prints a single slot with given values =============================
    def print_inventory_slot(k, uuid, full=True):
        print('[Slot ' + str(k) + '] | ', end='')
        if uuid is None:
            print('--empty--')
        elif uuid in Item.instances:
            if full:
                print()
                Item.instances[uuid].print_data()
            else:
                print(Item.instances[uuid].data['name'] + " [" + Item.instances[uuid].data['special_text'] + "]")

        else:
            print('--illegal uuid--')

    print_inventory_slot = staticmethod(print_inventory_slot)

    # prints player data =================================================
    def print_data_dict(self):
        for k in self.data:
            print(k + ": " + str(self.data[k]))
