from obj_data import Data
# from obj_utility import Utility
# from obj_item import Item, Upgradeable, Weapon, Equipment

class Game(object):
    __slots__ = ['used_uuids', 'players', 'gameobjects', 'npc', 'data']

    def __init__(self, data_files=None, game_state=None):
        if data_files is None:
            data_files = 'data_files.xml'
        if game_state is None:
            game_state = 'game_state.xml'
        self.used_uuids = list()
        self.data = Data(data_files)
        self.used_uuids.append(id(self.data))
        self.load_game_state(game_state)

    def load_game_state(self):
        raise NotImplementedError
