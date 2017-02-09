from obj_data import Data
from copy import copy


########################################################################################################################
# Class for all Items ==================================================================================================
class Item(object):
    # dict vor all Item-instances
    instances = dict()
    data_addresses = list()
    next_id = 0
    __slots__ = ['data', 'uuid']

    def __init__(self, item_id, item_data, regen_mem_location=True):
        # Generate uuid for item and store it for accessing later on
        self.uuid = Item.next_id
        Item.next_id += 1
        Item.instances[self.uuid] = self
        # 'loading' item data into data dict
        item_data, item_id = copy(item_data), copy(item_id)
        self.data = item_data
        self.data['item_id'] = item_id
        # Generating indepent datadict memory location to avoid memory overlap
        if regen_mem_location:
            while id(self.data) in Item.data_addresses:
                self.data = copy(self.data)
            Item.data_addresses.append(id(self.data))

    # subtracts a given value val from the items durability
    def sub_durability(self, val): self.data['durability'] -= val

    # prints the item data
    def print_data(self):
        print("Item | uuid: <" + str(self.uuid) + "> | itemid: <" + str(self.data['item_id']) + ">")
        print("~ lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
              "\n Weight: " + self.data['weight'] +
              "\n Price: " + self.data['price'] +
              "\n Specialtext: " + self.data['special_text'])

    # loads item data from player inventory save
    def set_specific_save_data(self, savedata):
        self.data['durability'] = savedata.attrib['durability']
        self.data['name'] = savedata.text if savedata.text != "none" else self.data['name']


# Parentclass for all upgradeable items ================================================================================
class Upgradeable(Item):
    def __init__(self, item_id, item_data, level=1, upgrade_path=None, equiptime="1", regen_mem_location=True):
        super().__init__(item_id, item_data, regen_mem_location=False)
        # 'loading' special data for upgradeables
        level, upgrade_path, equiptime = copy(level), copy(upgrade_path), copy(equiptime)
        self.data['level'] = level
        self.data['upgradepath'] = upgrade_path if upgrade_path is not None else dict()
        self.data['equiptime'] = equiptime
        # Generating indepent datadict memory location to avoid memory overlap
        if regen_mem_location:
            while id(self.data) in Item.data_addresses:
                self.data = copy(self.data)
            Item.data_addresses.append(id(self.data))

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

    # loads item data from player inventory save
    def set_specific_save_data(self, savedata):
        super().set_specific_save_data(savedata)
        if Data.is_number(savedata.attrib['level']):
            self.apply_levels(savedata.attrib['level'])
        else:
            self.level_up(savedata.attrib['level'])


# Class for all weapons ================================================================================================
class Weapon(Upgradeable):
    def __init__(self, item_id, item_data, weapon_data, size='medium', level=0):
        super().__init__(item_id, item_data, level, upgrade_path=weapon_data['upgradepath'],
                         equiptime=weapon_data['equiptime'], regen_mem_location=False)
        # 'loading' special data for weapons
        size, weapon_data = copy(size), copy(weapon_data)
        self.data['size'] = size
        self.data['weapon_type'] = weapon_data['type']
        self.data['base_damage'] = weapon_data['damage']
        self.data['damage_type'] = weapon_data['damage']['type']
        self.data['damage'] = weapon_data['damage'][size]
        self.data['range'] = weapon_data['range']
        self.apply_levels(level)
        # Generating indepent datadict memory location to avoid memory overlap
        while id(self.data) in Item.data_addresses:
            self.data = copy(self.data)
        Item.data_addresses.append(id(self.data))

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
        super().__init__(item_id, item_data, level=0, upgrade_path=equipment_data['upgradepath'],
                         equiptime=equipment_data['equiptime'], regen_mem_location=False)
        # 'loading' speical data for equipments
        equipment_data = copy(equipment_data)
        self.data['spellfailing'] = equipment_data['spellfailing']
        self.data['armordeficit'] = equipment_data['armordeficit']
        self.data['maxdexbonus'] = equipment_data['maxdexbonus']
        self.data['armor'] = equipment_data['armor']
        self.apply_levels(level)
        # Generating indepent datadict memory location to avoid memory overlap
        while id(self.data) in Item.data_addresses:
            self.data = copy(self.data)
        Item.data_addresses.append(id(self.data))

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
