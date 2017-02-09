from obj_game import Game
from obj_player import Player
from obj_item import Item


########################################################################################################################
game = Game()
player = Player("data/players/test.xml")

player.inventory['weapons'][2].apply_levels(6)
player.print_inventory(full=True)
