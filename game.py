import xml.etree.ElementTree as et
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
            return et.parse(path).getroot()
        except Exception as ex:
            print(ex)

    parse_file = staticmethod(parse_file)

    # Parsed alle nodes im XML-Objekt in ein dictionary
    def reparse_nodes(root):
        try:
            if not isinstance(root, et.Element):
                raise Exception(
                    'reparse_nodes: root is not a xml.etree.ElementTree.Element, root is ' + str(type(root)))
            raw_data = dict()
            for i, child in enumerate(root):
                raw_data[child.tag] = root[i]
            return raw_data
        except Exception as ex:
            print(ex)

    reparse_nodes = staticmethod(reparse_nodes)

    # prints a list of all instanciated items
    def print_intanciated_items():
        for key, item in Item.instances.items():
            print(str(key) + " --> " + item.data['name'])

    print_intanciated_items = staticmethod(print_intanciated_items)

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


########################################################################################################################
class Game(object):
    general = None

    def __init__(self, path="data_files.xml"):
        Game.general = self
        self.items = dict()
        self.talents = dict()
        self.races = dict()
        files = dict()
        for file in Data.parse_file(path):
            files[file.attrib['name']] = file.text

        self.parse_talents(Data.parse_file(files['talents']))
        self.parse_races(Data.parse_file(files['races']))
        self.parse_items(Data.parse_file(files['items']))
        self.parse_weapons(Data.parse_file(files['weapons']))
        self.parse_equipments(Data.parse_file(files['equipments']))

    # Parsing ==========================================================================================================
    # Parsing data on talents ===========================================
    def parse_talents(self, raw_data):
        for talent in raw_data:
            self.talents[talent.attrib['name']] = talent.text

    # Parsing data on races ==============================================
    def parse_races(self, raw_data):
        for race in raw_data:
            self.races[race.attrib['name']] = self.parse_race(race)

    # Parsing data for a single race ------
    def parse_race(self, raw_data):
        # Preparsing data for easier use
        data = Data.reparse_nodes(raw_data)
        race = dict()
        # Parsing talents
        race['talents'] = []
        for talent in data['talents']:
            if talent.text in self.talents:
                race['talents'].append(talent.text)

        # return finished parse result
        return race

    # Parsing data on items ==============================================
    def parse_items(self, raw_data):
        self.items['itemdata'] = dict()
        for item in raw_data:
            self.items['itemdata'][int(item.attrib['item_id'])] = self.parse_item(item)

    # Parsing data for a single item ------
    def parse_item(self, raw_data):
        # Preparing data for easier use
        data = Data.reparse_nodes(raw_data)
        item = dict()
        # Parsing Item data
        item['name'] = data['name'].text
        item['special_text'] = data['special_text'].text
        item['price'] = str(self.calc_price(float(data['price'].text), data['price'].attrib['scale']))
        item['weight'] = str(self.calc_weight(float(data['weight'].text), data['weight'].attrib['scale']))
        item['durability'] = int(data['durability'].text)
        return item

    # Parsing data on weapons ============================================
    def parse_weapons(self, raw_data):
        self.items['weapondata'] = dict()
        for weapon in raw_data:
            proposed_id_ref = int(weapon.attrib['item_id'])
            if proposed_id_ref in self.items['itemdata']:
                self.items['weapondata'][proposed_id_ref] = self.parse_weapon(weapon)

    # Parsing data for a single weapon ----
    def parse_weapon(self, raw_data):
        # Preparing data for easier use
        data = Data.reparse_nodes(raw_data)
        weapon = dict()
        # Parsing Weapon data
        weapon['type'] = {'hands': data['type'].attrib['hands'],
                          'rangend': data['type'].attrib['ranged'] == "1"}
        weapon['damage'] = {'very_small': data['damage'].attrib['very_small'],
                            'small': data['damage'].attrib['small'],
                            'medium': data['damage'].attrib['medium'],
                            'big': data['damage'].attrib['big'],
                            'type': data['damage'].attrib['type']}
        weapon['range'] = str(self.calc_length(float(data['range'].text), data['range'].attrib['scale']))
        weapon['equiptime'] = str(self.calc_time(float(data['equiptime'].text), data['equiptime'].attrib['scale']))
        weapon['upgradepath'] = dict()
        for upgradetree in data['upgradepath']:
            tree = dict()
            for upgrade in upgradetree:
                tree[upgrade.attrib['level']] = upgrade.text
            weapon['upgradepath'][upgradetree.tag] = tree
        return weapon

    # Parse data on equipments ===========================================
    def parse_equipments(self, raw_data):
        self.items['equipmentdata'] = dict()
        for equipment in raw_data:
            proposed_id_ref = int(equipment.attrib['item_id'])
            if proposed_id_ref in self.items['itemdata']:
                self.items['equipmentdata'][proposed_id_ref] = self.parse_equipment(equipment)

    # Parse data for a single equipment -
    def parse_equipment(self, raw_data):
        # Preparing data for easier use
        data = Data.reparse_nodes(raw_data)
        equipment = dict()
        # Parsing Equipment data
        equipment['spellfailing'] = data['spellfailing'].text
        equipment['armordeficit'] = data['armordeficit'].text
        equipment['maxdexbonus'] = data['maxdexbonus'].text
        equipment['armor'] = data['armor'].text
        equipment['equiptime'] = str(self.calc_time(float(data['equiptime'].text), data['equiptime'].attrib['scale']))
        equipment['upgradepath'] = dict()
        for upgradetree in data['upgradepath']:
            tree = dict()
            for upgrade in upgradetree:
                tree[upgrade.attrib['level']] = upgrade.text
            equipment['upgradepath'][upgradetree.tag] = tree
        return equipment

    # Calculating Data =================================================================================================
    # Calculating prices based on predetermined scale
    def calc_price(val, scale):
        return val * {"g": 10000,
                      "s": 100,
                      "c": 1}.get(scale, 1)

    calc_price = staticmethod(calc_price)

    # Calculating weights based on predetermined scale
    def calc_weight(val, scale):
        return val * {"t": 1000000,
                      "k": 1000,
                      "g": 1,
                      "m": 0.01}.get(scale, 1)

    calc_weight = staticmethod(calc_weight)

    # Calculating distances based on predetermined scale
    def calc_length(val, scale):
        return val * {"k": 1000,
                      "m": 1,
                      "d": 0.1,
                      "c": 0.01}.get(scale, 1)

    calc_length = staticmethod(calc_length)

    # Calculating times based on predetermined scale
    def calc_time(val, scale):
        return val * {"t": 1,
                      "m": 4}.get(scale, 1)

    calc_time = staticmethod(calc_time)

    # Getter für einzelne Items als Objekte aus ========================================================================
    def item(self, item_id):
        return Item(item_id, self.items['itemdata'][item_id])

    def weapon(self, item_id):
        return Weapon(item_id, self.items['itemdata'][item_id], self.items['weapondata'][item_id])

    def equipment(self, item_id):
        return Equipment(item_id, self.items['itemdata'][item_id], self.items['equipmentdata'][item_id])

    # Debugging ========================================================================================================
    # prints all items
    def print_items(self):
        print("[ITEMS]")
        for item_id, data in self.items['itemdata'].items():
            print("<ID: " + str(item_id) + ">")
            Data.print_dict(data)

    # prints all wepaons in itemdata and weapondata
    def print_weapons(self):
        print("[WEAPONS]")
        for item_id, data in self.items['weapondata'].items():
            print("<ID: " + str(item_id) + ">\n--> Itemdata: ")
            Data.print_dict(self.items['itemdata'][item_id])
            print("--> Weapondata: ")
            Data.print_dict(data)

    # prints all equipments in itemdata and equipmentdata
    def print_equipments(self):
        print("[EQUIPMENTS]")
        for item_id, data in self.items['equipmentdata'].items():
            print("<ID: " + str(item_id) + ">\n--> Itemdata: ")
            Data.print_dict(self.items['itemdata'][item_id])
            print("--> Equipmentdata: ")
            Data.print_dict(data)

    # prints all races
    def print_races(self):
        print("[RACES]")
        for name, data in self.races.items():
            print("<name: " + name + ">\n--> Data: " + str(data))

    # prints all talents
    def print_talents(self):
        print("[TALENTS]")
        for name, data in self.talents.items():
            print("<name: " + name + ">\n--> Data: " + str(data))


########################################################################################################################
# Class for all Items ==================================================================================================
class Item(object):
    # dict vor all Item-instances
    instances = dict()
    next_id = 0

    def __init__(self, item_id, item_data):
        self.uuid = Item.next_id
        Item.next_id += 1
        Item.instances[self.uuid] = self
        self.data = dict()
        self.data = item_data
        self.data['item_id'] = item_id

    # subtracts a given value val from the items durability
    def sub_durability(self, val): self.data['durability'] -= val

    # prints the item data
    def print_data(self):
        print("Item | uuid: <" + str(self.uuid) + "> | itemid: <" + str(self.data['item_id']) + ">")
        print("~ lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
              "\n Weight: " + self.data['weight'] +
              "\n Price: " + self.data['price'] +
              "\n Specialtext: " + self.data['special_text'])


# Parentclass for all upgradeable items ================================================================================
class Upgradeable(Item):
    def __init__(self, item_id, item_data, level=1, upgrade_path=None, equiptime="1"):
        self.data = dict()
        super().__init__(item_id, item_data)
        self.data['level'] = level
        self.data['upgradepath'] = upgrade_path if upgrade_path is not None else dict()
        self.data['equiptime'] = equiptime

    # applies upgrade for either the next level or a given level
    def level_up(self, level=None):
        if level is None:
            if not Data.is_number(self.data['level']):
                return
            self.data['level'] += 1
            level = self.data['level']
        else:
            self.data['level'] = level
        for tree in self.data['upgradepath']:
            if tree in self.data and str(level) in self.data['upgradepath'][tree]:
                self.data[tree] = self.data[tree] + " (" + self.data['upgradepath'][tree][str(level)] + ")"

    # applies the next x level upgrades
    def apply_levels(self, limit=1):
        for i in range(self.data['level'], self.data['level'] + int(limit)):
            self.level_up()


# Class for all weapons ================================================================================================
class Weapon(Upgradeable):
    def __init__(self, item_id, item_data, weapon_data, size='medium', level=0):
        self.data = dict()
        super().__init__(item_id, item_data, level, upgrade_path=weapon_data['upgradepath'],
                         equiptime=weapon_data['equiptime'])
        self.data['size'] = size
        self.data['weapon_type'] = weapon_data['type']
        self.data['base_damage'] = weapon_data['damage']
        self.data['damage_type'] = weapon_data['damage']['type']
        self.data['damage'] = weapon_data['damage'][size]
        self.data['range'] = weapon_data['range']
        self.apply_levels(level)

    # prints weapon and item data
    def print_data(self):
        print("Item->Equipable->Weapon | uuid: <" + str(self.uuid) + "> | itemid: <" + str(self.data['item_id']) + ">")
        print(
            str(self.data['level']) + " lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
            "\n Weight: " + self.data['weight'] +
            "\n Price: " + self.data['price'] +
            "\n Specialtext: " + self.data['special_text'] +
            "\n Damage: " + self.data['damage'] +
            "\n Size: " + self.data['size'] +
            "\n Weapontype: " + str(self.data['weapon_type']) +
            "\n Damagetype: " + self.data['damage_type'] +
            "\n Range: " + self.data['range'] +
            "\n Upgradepaths: ")
        for path in self.data['upgradepath']:
            print("   " + path + ": " + str(self.data['upgradepath'][path]))


# Class for all equipments =============================================================================================
class Equipment(Upgradeable):
    def __init__(self, item_id, item_data, equipment_data, level=0):
        self.data = dict()
        super().__init__(item_id, item_data, level, upgrade_path=equipment_data['upgradepath'],
                         equiptime=equipment_data['equiptime'])
        self.data['spellfailing'] = equipment_data['spellfailing']
        self.data['armordeficit'] = equipment_data['armordeficit']
        self.data['maxdexbonus'] = equipment_data['maxdexbonus']
        self.data['armor'] = equipment_data['armor']
        self.apply_levels(1)

    # prints equipment and item data
    def print_data(self):
        print("Item->Equipable->Equipment | uuid: <" + str(self.uuid) +
              "> | itemid: <" + str(self.data['item_id']) + ">")
        print(
            str(self.data['level']) + " lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
            "\n Weight: " + self.data['weight'] +
            "\n Price: " + self.data['price'] +
            "\n Specialtext: " + self.data['special_text'] +
            "\n Armor: " + self.data['armor'] +
            "\n Spellfailing chance: " + self.data['spellfailing'] +
            "\n Armordeficit: " + self.data['armordeficit'] +
            "\n Maximum Dexterity Bonus: " + self.data['maxdexbonus'] +
            "\n Upgradepaths: ")
        for path in self.data['upgradepath']:
            print("   " + path + ": " + str(self.data['upgradepath'][path]))


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
                self.add_item_to_inventory(self.parse_item(child))
            elif child.tag == "weapon":
                self.add_item_to_inventory(self.parse_weapon(child))
            elif child.tag == "equipment":
                self.add_item_to_inventory(self.parse_equipment(child))

    def parse_item(self, data):
        item = self.parent.item(int(data.attrib['itemid']))
        item.data['durability'] = data.attrib['durability']
        if data.text != "none":
            item.data['name'] = data.text
        return item.uuid

    # parsing weapons ====================================================
    def parse_weapons(self, raw_data):
        for child in raw_data:
            self.equip_item(self.parse_weapon(child))

    def parse_weapon(self, data):
        weapon = self.parent.weapon(int(data.attrib['itemid']))
        uuid = weapon.uuid
        Item.instances[uuid].data['durability'] = data.attrib['durability']
        if data.text != "none":
            Item.instances[uuid].data['name'] = data.text
        if Data.is_number(data.attrib['level']):
            Item.instances[uuid].apply_levels(data.attrib['level'])
        else:
            Item.instances[uuid].level_up(data.attrib['level'])
        return uuid

    # parsing equipments =================================================
    def parse_equipments(self, raw_data):
        for child in raw_data:
            self.equip_item(self.parse_equipment(child))

    def parse_equipment(self, data):
        equipment = self.parent.equipment(int(data.attrib['itemid']))
        uuid = equipment.uuid
        equipment.data['durability'] = data.attrib['durability']
        if data.text != "none":
            Item.instances[uuid].data['name'] = data.text
        if Data.is_number(data.attrib['level']):
            Item.instances[uuid].apply_levels(data.attrib['level'])
        else:
            Item.instances[uuid].level_up(data.attrib['level'])
        return uuid

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


########################################################################################################################
game = Game()
player = Player("data/players/test.xml")

player.print_inventory()
print(Item.instances)
