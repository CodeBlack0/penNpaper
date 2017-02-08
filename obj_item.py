from obj_data import Data


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
