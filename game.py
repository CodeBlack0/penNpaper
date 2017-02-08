import xml.etree.ElementTree as ET


########################################################################################################################
class Data():
    def __init__(self, path="data_files.xml"):
        self.items = dict()
        self.talents = dict()
        self.races = dict()
        files = dict()
        for file in self.parse_file(path):
            files[file.attrib['name']] = file.text
        self.parse_talents(self.parse_file(files['talents']))
        self.parse_races(self.parse_file(files['races']))
        self.parse_items(self.parse_file(files['items']))
        self.parse_weapons(self.parse_file(files['weapons']))
        self.parse_equipments(self.parse_file(files['equipments']))

    # Parsing ==========================================================================================================
    # Parsing XML File
    def parse_file(path):
        return ET.parse(path).getroot()
    parse_file = staticmethod(parse_file)

    # Parsed alle nodes im XML-Objekt in ein dictionary
    def reparse_nodes(root):
        raw_data = dict()
        for i, child in enumerate(root):
            raw_data[child.tag] = root[i]
        return raw_data
    reparse_nodes = staticmethod(reparse_nodes)

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
        data = self.reparse_nodes(raw_data)
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
        data = self.reparse_nodes(raw_data)
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
        data = self.reparse_nodes(raw_data)
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
        data = self.reparse_nodes(raw_data)
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
    # Berechnet Preise in einheitliche Werte
    def calc_price(val, scale):
        return val * {"g": 10000,
                      "s": 100,
                      "c": 1}.get(scale, 1)
    calc_price = staticmethod(calc_price)

    # Berechnet Gewichte in einheitliche Werte
    def calc_weight(val, scale):
        return val * {"t": 1000000,
                      "k": 1000,
                      "g": 1,
                      "m": 0.01}.get(scale, 1)
    calc_weight = staticmethod(calc_weight)

    # Berechnet Längen in einheitliche Werte
    def calc_length(val, scale):
        return val * {"k": 1000,
                      "m": 1,
                      "d": 0.1,
                      "c": 0.01}.get(scale, 1)
    calc_length = staticmethod(calc_length)

    # Berechnet Zeiten in einheitliche Werte
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
    # Druckt ein dict()ionary aus
    def print_dict(item):
        for k, data in item.items():
            print(str(k) + ': ' + str(data))
    print_dict = staticmethod(print_dict)

    # Druckt alle Items aus
    def print_items(self):
        print("[ITEMS]")
        for item_id, data in self.items['itemdata'].items():
            print("<ID: " + str(item_id) + ">")
            self.print_dict(data)

    # Druckt alle Waffen aus
    def print_weapons(self):
        print("[WEAPONS]")
        for item_id, data in self.items['weapondata'].items():
            print("<ID: " + str(item_id) + ">\n--> Itemdata: ")
            self.print_dict(self.items['itemdata'][item_id])
            print("--> Weapondata: ")
            self.print_dict(data)

    # Druckt alle ausrüstbaren Gegstände aus
    def print_equipments(self):
        print("[EQUIPMENTS]")
        for item_id, data in self.items['equipmentdata'].items():
            print("<ID: " + str(item_id) + ">\n--> Itemdata: ")
            self.print_dict(self.items['itemdata'][item_id])
            print("--> Equipmentdata: ")
            self.print_dict(data)

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

    def print_intanciated_items():
        for key, item in Item.instances.items():
            print(str(key) + " --> " + item.data['name'])
    print_intanciated_items = staticmethod(print_intanciated_items)


########################################################################################################################
# Classe für alle Items ================================================================================================
class Item():
    # dict() aller Item-Instancen
    instances = dict()

    def __init__(self, item_id, item_data):
        self.uuid = id(self)
        Item.instances[self.uuid] = self
        self.data = item_data
        self.data['item_id'] = item_id

    # Zieht von der Haltbarkeit eines Items einen gegebene Wert ab
    def sub_durability(self, val): self.data['durability'] -= val

    # Druckt alle Infos zum Item aus
    def print_data(self):
        print("Item | uuid: <" + str(self.uuid) + "> | itemid: <" + str(self.data['item_id']) + ">")
        print(
            str(self.data['level']) + " lvl | " + self.data['name'] + " | durability: " + str(self.data['durability']) +
            "\n Weight: " + self.data['weight'] +
            "\n Price: " + self.data['price'] +
            "\n Specialtext: " + self.data['special_text'])


# Parentclasse für alle ausrüstbaren Items =============================================================================
class Equipable(Item):
    def __init__(self, item_id, item_data, level=1, upgrade_path=None, equiptime="1"):
        super().__init__(item_id, item_data)
        self.data['level'] = level
        self.data['upgradepath'] = upgrade_path if upgrade_path is not None else dict()
        self.data['equiptime'] = equiptime

    # Wendet den vorgegebenen Level-Up Pfad eines ausrüstbaren Items an
    def level_up(self, level=False):
        if not level:
            self.data['level'] += 1
            level = self.data['level']
        else:
            self.data['level'] = level
        for tree in self.data['upgradepath']:
            if tree in self.data and str(level) in self.data['upgradepath'][tree]:
                self.data[tree] = self.data[tree] + " (" + self.data['upgradepath'][tree][str(level)] + ")"

    # Wendet eine gegebene Anzahl an Levels an
    def apply_levels(self, limit=1):
        for level in range(self.data['level'], self.data['level'] + limit):
            if level != 1: self.level_up(level)


# Classe für alle Waffen ===============================================================================================
class Weapon(Equipable):
    def __init__(self, item_id, item_data, weapon_data, size='medium', level=0):
        super().__init__(item_id, item_data, level, upgrade_path=weapon_data['upgradepath'],
                         equiptime=weapon_data['equiptime'])
        self.data['size'] = size
        self.data['weapon_type'] = weapon_data['type']
        self.data['base_damage'] = weapon_data['damage']
        self.data['damage_type'] = weapon_data['damage']['type']
        self.data['damage'] = weapon_data['damage'][size]
        self.data['range'] = weapon_data['range']
        self.apply_levels(level)

    # Druckt alle Infos zur Waffe aus
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


# Classe für alle Rüstungen etc. =======================================================================================
class Equipment(Equipable):
    def __init__(self, item_id, item_data, equipment_data, level=0):
        super().__init__(item_id, item_data, level, upgrade_path=equipment_data['upgradepath'],
                         equiptime=equipment_data['equiptime'])
        self.data['spellfailing'] = equipment_data['spellfailing']
        self.data['armordeficit'] = equipment_data['armordeficit']
        self.data['maxdexbonus'] = equipment_data['maxdexbonus']
        self.data['armor'] = equipment_data['armor']
        self.apply_levels(1)

    # Druckt alle Infos zur Rüstung o.ä. aus
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
# Classe zum verwalten von Spielerdaten
class Player(object):
    # dict() für alle Player-Instancen
    instances = dict()

    def __init__(self, path=None):
        self.uuid = id(self)
        Player.instances[self.uuid] = self

        self.inventory = {
            "contents": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None},
            "weapons": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None},
            "equipment": {1: None, 2: None, 3: None, 4: None},
            "weight": 0}
        if isinstance(path, str):
            tree = ET.parse(path)
            root = tree.getroot()

            raw_data = dict()
            for i, child in enumerate(root):
                raw_data[child.tag] = root[i]

            self.data = dict()
            stats = dict()
            for child in raw_data['stats'][0]:
                stats[child.tag] = child.text
            stats['rolled'] = dict()
            for child in raw_data['stats'][1][0]:
                stats['rolled'][child.tag] = int(child.text)
            stats['other'] = dict()
            for child in raw_data['stats'][1][1]:
                stats['other'][child.tag] = int(child.text)

            self.data['stats'] = stats

        else:
            print("Failed to initialize Player from " + str(path))

    # Druckt alle Spielerdaten aus =====================================================================================
    def print_data_dict(self):
        for k in self.data:
            print(k + ": " + str(self.data[k]))

    # Fügt ein Item dem Inventar hinzu (anhand der uuid, gibt den 'Erfolg' zurück) =====================================
    def add_item_to_inventory(self, item, slot='contents'):
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

    # Entfernt ein Item aus dem Inventar (gibt das Item zurück) ========================================================
    def remove_item_from_inventory(self, index):
        if index not in self.inventory['contents']: return False
        temp, self.inventory['contents'][index] = self.inventory['contents'][index], None
        return temp

    # Rüstet einen Gegenstand aus (anhand der uuid, gibt den 'Erfolg' zurück
    def equip_item(self, uuid):
        if uuid is None:
            return False
        if isinstance(uuid, Item):
            uuid = uuid.uuid
        if isinstance(Item.instances[uuid], Weapon):
            return self.add_item_to_inventory(uuid, slot='weapons')
        if isinstance(Item.instances[uuid], Equipment):
            return self.add_item_to_inventory(uuid, slot='equipment')
        else:
            return False

    # Rüstet einen Gegestand von Inventar aus (anhand des Indexes des Items in Inventar, gibt den 'Erfolg' zurück) =====
    def equip_from_inventory(self, index):
        if isinstance(Item.instances[self.inventory['contents'][index]], Equipable):
            return self.equip_item(self.remove_item_from_inventory(index))
        else:
            return False

    # Druckt das Inventar eines Spieler aus ============================================================================
    def print_inventory(self, full=False):
        print('----[Player Inventory][Player UUID: ' + str(self.uuid) + ']---- \n<-- [Bag] -->')
        for k, uuid in self.inventory['contents'].items():
            self.print_inventory_slot(k, uuid, full)
        print('<-- [Weapons] -->')
        for k, uuid in self.inventory['weapons'].items():
            self.print_inventory_slot(k, uuid, full)
        print('<-- [Equipment] -->')
        for k, uuid in self.inventory['equipment'].items():
            self.print_inventory_slot(k, uuid, full)

    # Druckt ein einzelnes Item aus
    # (anhand der uuid, kann zwischen vollständiger und gekürtzter darstellung unterscheiden) ==========================
    def print_inventory_slot(k, uuid, full=True):
        print('[Slot ' + str(k) + '] | ', end='')
        if uuid is None:
            print('--empty--')
        elif uuid in Item.instances:
            if full:
                Item.instances[uuid].print_data()
            else:
                print(Item.instances[uuid].data['name'])
        else:
            print('--illegal uuid--')
    print_inventory_slot = staticmethod(print_inventory_slot)


######################################################################
player = Player("data/players/test.xml")
data = Data()

index1 = player.add_item_to_inventory(data.item(2))
index2 = player.add_item_to_inventory(data.item(3))
index3 = player.add_item_to_inventory(data.weapon(4))
player.equip_from_inventory(index1)
player.equip_from_inventory(index2)
player.equip_from_inventory(index3)
player.equip_item(data.equipment(5))
player.print_inventory()
