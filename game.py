import xml.etree.ElementTree as ET

######################################################################
class Data():
  
  def __init__(self, path=False):
    if isinstance(path, str):
      tree = ET.parse(path)
      root = tree.getroot()

      raw_data = {}    
      for i, child in enumerate(root):
         raw_data[child.tag] = root[i]

      self.talents = []
      for child in raw_data['talents']:
        self.talents.append(child.text)   

      self.races = {} 
      for child in raw_data['races']:
         race = {}
         # Getting raw data
         race_data = {}
         for i, data in enumerate(child):
           race_data[data.tag] = child[i]
         # Parsing race talents
         race['talents'] = []
         for data in race_data['talents']:
           if data.text in self.talents:
             race['talents'].append(self.talents.index(data.text))
         # Parsing base_stats
         
         # Adding Race to race_dict
         self.races[child.tag] = race
   

  def get_races(self):
    return self.races

  def get_talents(self):
    return self.talents

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
data = Data("data.xml")
talents = data.get_talents()
races = data.get_races()

player = Player("test.xml")
for talent in races[player.get_data()['stats']['race']]['talents']:
  print(talents[talent])
























