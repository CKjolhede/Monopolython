from models.__init__ import CONN, CURSOR
from models.game import Game
from models.space import Space
from models.player import Player
from models.game_space import Game_space
from models.setup_helper import (seed_spaces)
from sqlite3 import *

def migrate():
    Game.drop_table()
    Space.drop_table()
    Game_space.drop_table()
    Player.drop_table()
    print("Tables have been dropped")
    Game_space.create_table()
    Game.create_table()
    Space.create_table()
    Player.create_table()
    print("Tables have been created")
    


if __name__ == "__main__":
    migrate()
    seed_spaces()