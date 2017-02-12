from old.obj_game import Game
from old.obj_player import Player

########################################################################################################################
game = Game()
player = Player("data/players/test.xml")

player.print_inventory(full=True)

