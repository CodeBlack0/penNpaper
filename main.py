from obj_game import Game
from obj_player import Player
from obj_item import Item


########################################################################################################################
game = Game()
player = Player("data/players/test.xml")

print(Item.data_addresses)
player.print_inventory(full=True)
