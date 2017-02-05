import xml.etree.ElementTree as ET
from enum import Enum


######################################################################
class Data():
    def __init__(self, paths={"races": "races.xml",
                              "talents": "talents.xml",
                              "items": "items.xml",
                              "weapons": "weapons.xml",
                              "equipments": "equipments.xml"}):
        self.parse_talents(self.parse_file(paths['talents']))
        self.parse_races(self.parse_file(paths['races']))
        self.parse_items(self.parse_file(paths['items']))
        self.parse_weapons(self.parse_file(paths['weapons']))
        self.parse_equipments(self.parse_file(paths['equipments']))

    # Parsing ------------------------------------------------------------
    # Parsing XML File --------------------
    def parse_file(self, path):
        return ET.parse(path).getroot()

    # Parsing data on talents -------------
    def parse_talents(self, raw_data):
        self.talents = {}
        for talent in raw_data:
            self.talents[talent.attrib['name']] = talent.text

    # Parsing data on races ---------------
    def parse_races(self, raw_data):
        self.races = {}
        for race in raw_data:
            self.races[race.attrib['name']] = self.parse_race(race)

    # Parsing data for a single race ------
    def parse_race(self, raw_data):
        # Preparsing data for easier use
        data = self.reparse_nodes(raw_data)
        race = {}
        # Parsing talents
        race['talents'] = []
        for talent in data['talents']:
            if talent.text in self.talents:
                race['talents'].append(talent.text)

        # return finished parse result
        return race

    # Parsing data on items ---------------
    def parse_items(self, raw_data):
        self.items = {}
        for item in raw_data:
            self.items[int(item.attrib['id'])] = self.parse_item(item)

    # Parsing data for a single item ------
    def parse_item(self, raw_data):
        # Preparing data for easier use
        data = self.reparse_nodes(raw_data)
        item = {}
        # Parsing Item data
        item['name'] = data['name'].text
        item['special_text'] = data['special_text'].text
        item['price'] = str(self.calc_price(float(data['price'].text), data['price'].attrib['scale']))
        item['weight'] = str(self.calc_weight(float(data['weight'].text), data['weight'].attrib['scale']))
        item['durability'] = int(data['durability'].text)
        return item

    # Parsing data on weapons -------------
    def parse_weapons(self, raw_data):
        self.weapons = {}
        for weapon in raw_data:
            proposed_id_ref = int(weapon.attrib['item_id'])
            if proposed_id_ref in self.items:
                self.weapons[proposed_id_ref] = self.parse_weapon(weapon)

    # Parsing data for a single weapon ----
    def parse_weapon(self, raw_data):
        # Preparing data for easier use
        data = self.reparse_nodes(raw_data)
        weapon = {}
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
        weapon['upgradepath'] = {}
        for upgradetree in data['upgradepath']:
            tree = {}
            for upgrade in upgradetree:
                tree[upgrade.attrib['level']] = upgrade.text
            weapon['upgradepath'][upgradetree.tag] = tree
        return weapon

    # Parse data on equipments ------------
    def parse_equipments(self, raw_data):
        self.equipments = {}
        for equipment in raw_data:
            proposed_id_ref = int(equipment.attrib['item_id'])
            if proposed_id_ref in self.items:
                self.equipments[proposed_id_ref] = self.parse_equipment(equipment)

    # Parse data for a single equipment -
    def parse_equipment(self, raw_data):
        # Preparing data for easier use
        data = self.reparse_nodes(raw_data)
        equipment = {}
        # Parsing Equipment data
        equipment['spellfailing'] = data['spellfailing'].text
        equipment['armordeficit'] = data['armordeficit'].text
        equipment['maxdexbonus'] = data['maxdexbonus'].text
        equipment['armor'] = data['armor'].text
        equipment['equiptime'] = str(self.calc_time(float(data['equiptime'].text), data['equiptime'].attrib['scale']))
        equipment['upgradepath'] = {}
        for upgradetree in data['upgradepath']:
            tree = {}
            for upgrade in upgradetree:
                tree[upgrade.attrib['level']] = upgrade.text
            equipment['upgradepath'][upgradetree.tag] = tree
        return equipment


    # Parsed alle nodes im XML-Objekt in ein Dictionary
    def reparse_nodes(self, root):
        raw_data = {}
        for i, child in enumerate(root):
            raw_data[child.tag] = root[i]
        return raw_data

    # Calculating Data ---------------------------------------------------
    # Berechnet Preise in einheitliche Werte
    def calc_price(self, val, scale):
        return val * {"g": 10000,
                      "s": 100,
                      "k": 1}.get(scale, 1)

    # Berechnet Gewichte in einheitliche Werte
    def calc_weight(self, val, scale):
        return val * {"t": 1000000,
                      "k": 1000,
                      "g": 1,
                      "m": 0.01}.get(scale, 1)

    # Berechnet Längen in einheitliche Werte
    def calc_length(self, val, scale):
        return val * {"k": 1000,
                      "m": 1,
                      "d": 0.1,
                      "c": 0.01}.get(scale, 1)

    # Berechnet Zeiten in einheitliche Werte
    def calc_time(self, val, scale):
        return val * {"t": 1,
                      "m": 4}.get(scale, 1)

    # Getter für einzelne Items als Objekte aus --------------------------
    def item(self, id): return Item(id, self.items[id])

    def weapon(self, id): return Weapon(id, self.items[id], self.weapons[id])

    def equipment(self, id): return Equipment(id, self.items[id], self.equipments[id])

    # Debugging ----------------------------------------------------------
    # Druckt alle Items aus
    def print_items(self):
        print("[ITEMS]")
        for id, data in self.items.items():
            print("<ID: " + str(id) + ">\n--> Data: " + str(data))

    # Druckt alle Waffen aus
    def print_weapons(self):
        print("[WEAPONS]")
        for id, data in self.weapons.items():
            print("<ID: " + str(id) + ">\n--> Itemdata: " + str(self.items[id]) + "\n--> Weapondata: " + str(data))

    # Druckt alle ausrüstbaren Gegstände aus
    def print_equipments(self):
        print("[EQUIPMENTS]")
        for id, data in self.equipments.items():
            print("<ID: " + str(id) + ">\n--> Itemdata: " + str(self.items[id]) + "\n--> Equipdata: " + str(data))

    # Druckt alle Rassen aus
    def print_races(self):
        print("[RACES]")
        for name, data in self.races.items():
            print("<name: " + name + ">\n--> Data: " + str(data))

    # Druckt alle Talente aus
    def print_talents(self):
        print("[TALENTS]")
        for name, data in self.talents.items():
            print("<name: " + name + ">\n--> Data: " + str(data))


#####################################################################
class Item():
    def __init__(self, id, item_data):
        self.data = item_data
        self.data['id'] = id

    def sub_durability(self, val): self.data['durability'] -= val

class Equipable(Item):
    def __init__(self, id, item_data, level=1, upgrade_path={}, equiptime="1"):
        super().__init__(id, item_data)
        self.data['level'] = level
        self.data['upgradepath'] = upgrade_path
        self.data['equiptime'] = equiptime

    def level_up(self, level=False):
        if not level:
            self.data['level'] += 1
            level = self.data['level']
        else:
            self.data['level'] = level
        for tree in self.data['upgradepath']:
            if tree in self.data and str(level) in self.data['upgradepath'][tree]:
                self.data[tree] = self.data[tree] + " (" + self.data['upgradepath'][tree][str(level)] + ")"

    def apply_levels(self, limit=False):
        if not limit:
            limit = 1
        for level in range(self.data['level'], self.data['level']+limit):
            if level != 1: self.level_up(level)

class Weapon(Equipable):
    def __init__(self, id, item_data, weapon_data, size='medium', level=0):
        super().__init__(id, item_data, level, upgrade_path=weapon_data['upgradepath'], equiptime=weapon_data['equiptime'])
        self.data['size'] = size
        self.data['weapon_type'] = weapon_data['type']
        self.data['base_damage'] = weapon_data['damage']
        self.data['damage_type'] = weapon_data['damage']['type']
        self.data['damage'] = weapon_data['damage'][size]
        self.data['range'] = weapon_data['range']
        self.apply_levels(level)

    def print_data(self):
        print(str(self.data['level']) + " lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
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


class Equipment(Equipable):
    def __init__(self, id, item_data, equipment_data, level=0):
        super().__init__(id, item_data, level, upgrade_path=equipment_data['upgradepath'], equiptime=equipment_data['equiptime'])
        self.data['spellfailing'] = equipment_data['spellfailing']
        self.data['armordeficit'] = equipment_data['armordeficit']
        self.data['maxdexbonus'] = equipment_data['maxdexbonus']
        self.data['armor'] = equipment_data['armor']
        self.apply_levels(1)

    def print_data(self):
        print(str(self.data['level']) + " lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
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

######################################################################
class Player():
    def __init__(self, path=False):
        self.inventory = []
        self.weapons = []
        self.equipment = []
        if isinstance(path, str):
            tree = ET.parse(path)
            root = tree.getroot()

        raw_data = {}
        for i, child in enumerate(root):
            raw_data[child.tag] = root[i]

        self.data = {}
        stats = {}
        for child in raw_data['stats'][0]:
            stats[child.tag] = child.text
        stats['rolled'] = {}
        for child in raw_data['stats'][1][0]:
            stats['rolled'][child.tag] = int(child.text)
        stats['other'] = {}
        for child in raw_data['stats'][1][1]:
            stats['other'][child.tag] = int(child.text)

        self.data['stats'] = stats

    def print_data_dict(self):
        for k in self.data:
            print(k + ": " + str(self.data[k]))


######################################################################
player = Player("test.xml")
data = Data()

irondagger = data.weapon(4)
irondagger.apply_levels(5)
irondagger.print_data()
print("----------------------------------------")

leathershoulders = data.equipment(5)
leathershoulders.print_data()
print("----------------------------------------")
leathershoulders.apply_levels(2)
leathershoulders.print_data()
print("----------------------------------------")
leathershoulders.level_up("GODHOOD")
print(str(leathershoulders.data['level']) + " lvl | " +  leathershoulders.data['name'] + "\n" +
      leathershoulders.data['special_text'] + "\n" +
      leathershoulders.data['armor'])
print("----------------------------------------")