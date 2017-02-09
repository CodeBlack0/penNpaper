from obj_data import Data
from obj_item import Item, Weapon, Equipment


########################################################################################################################
class Game(object):
    general = None
    __slots__ = ['items', 'talents', 'races']

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
