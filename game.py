import xml.etree.ElementTree as ET
from enum import Enum

######################################################################
class Data():
  
  def __init__(self, paths={"races":"races.xml", "talents":"talents.xml", "items":"items.xml", "weapons":"weapons.xml"}):
    self.parse_talents(self.parse_file(paths['talents']))
    self.parse_races(self.parse_file(paths['races']))
    self.parse_items(self.parse_file(paths['items']))
    self.parse_weapons(self.parse_file(paths['weapons']))

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
    item['price'] = self.calc_price(float(data['price'].text), data['price'].attrib['scale'])
    item['weight'] = self.calc_weight(float(data['weight'].text), data['weight'].attrib['scale'])
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
    weapon['type'] = {'hands':data['type'].attrib['hands'],
                      'rangend':data['type'].attrib['ranged'] == "1"}
    weapon['damage'] = {'very_small':data['damage'].attrib['very_small'],
                        'small':data['damage'].attrib['small'],
                        'medium':data['damage'].attrib['medium'],
                        'big':data['damage'].attrib['big']}
    weapon['range'] = self.calc_length(float(data['range'].text), data['range'].attrib['scale'])
    weapon['equiptime'] = self.calc_time(float(data['equiptime'].text), data['equiptime'].attrib['scale'])
    return weapon
  
  
  # Parsed alle nodes im XML-Objekt in ein Dictionary
  def reparse_nodes(self, root):
    raw_data = {}
    for i, child in enumerate(root):
      raw_data[child.tag] = root[i]
    return raw_data

# Calculating Data ---------------------------------------------------
  # Berechnet Preise in einheitliche Werte
  def calc_price(self, val, scale):
    return val * { "g":10000,
                   "s":100,
                   "k":1}.get(scale, 1)

  # Berechnet Gewichte in einheitliche Werte
  def calc_weight(self, val, scale):
    return val * { "t":1000000,
                   "k":1000,
                   "g":1,
                   "m":0.01}.get(scale, 1)

  # Berechnet Längen in einheitliche Werte
  def calc_length(self, val, scale):
    return val * { "k":1000,
                   "m":1,
                   "d":0.1,
                   "c":0.01}.get(scale, 1)

  # Berechnet Zeiten in einheitliche Werte
  def calc_time(self, val, scale):
    return val * { "t":1,
                   "m":4}.get(scale, 1)

# Data-Getters -------------------------------------------------------
  # Getter für races-dict
  def get_races(self):
    return self.races

  # Getter für talents-dict
  def get_talents(self):
    return self.talents

  # Getter für items-dict
  def get_items(self):
    return self.items

  # Getter für weapons-dict
  def get_weapons(self):
    return self.weapons

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
    self.id = id
    self.name = item_data['name']
    self.weight = item_data['weight']
    self.price = item_data['price']
    self.special_text = item_data['special_text']
    self.durability = item_data['durability']

  def get_name(self):
    return self.name

  def get_weight(self):
    return self.weight

  def get_price(self):
    return self.price

  def get_special_text(self):
    return self.special_text

  def get_durability(self):
    return self.durability

  def sub_durability(self, val):
    self.durability -= val

class Weapon(Item):

  def __init__(self, weapon_data):
    super().__init__(weapon_data)


######################################################################
class Player():
  
  def __init__(self, path=False):
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

  def get_data(self):
    return self.data

######################################################################
player = Player("test.xml")
data = Data()
talents = data.get_talents()
races = data.get_races()
items = data.get_items()

data.print_items()
data.print_races()
data.print_talents()
data.print_weapons()