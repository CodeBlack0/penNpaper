import xml.etree.ElementTree as ET
from enum import Enum

######################################################################
class Data():
  
  def __init__(self, paths={"races":"races.xml", "talents":"talents.xml"}):
     self.parse_talents(self.parse_file(paths['talents']))
     self.parse_races(self.parse_file(paths['races']))

  def parse_file(self, path):
    return ET.parse(path).getroot()

  def parse_talents(self, raw_data):
    self.talents = {}
    for talent in raw_data:
      self.talents[talent.attrib['name']] = talent.text

  def parse_races(self, raw_data):
    self.races = {}
    for race in raw_data:
       self.races[race.attrib['name']] = self.parse_race(race)

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

  def reparse_nodes(self, root):
    raw_data = {}
    for i, child in enumerate(root):
      raw_data[child.tag] = root[i]
    return raw_data

  def get_races(self):
    return self.races

  def get_talents(self):
    return self.talents

#####################################################################
class Item():

  def __init__(self, raw_data):
    data = {}
    for i, child in enumerate(raw_data):
      data[child.tag] = raw_data[i]

    self.name = data['name']
    self.weight = int(data['weight'])
    self.price = int(data['price'])
    self.special_text = data['special_text']
    self.durability = data['durability']

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

  def __init__(self, raw_data):
    super().__init__(raw_data[0])
    data = {}
    for i, child in raw_data[1]:
      data[child.tag] = raw_data[1][i]




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
data = Data()
talents = data.get_talents()
races = data.get_races()

player = Player("test.xml")
for talent in races[player.get_data()['stats']['race']]['talents']:
  print(talent)