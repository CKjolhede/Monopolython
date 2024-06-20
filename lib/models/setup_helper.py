# lib/helper.py
import time
from sqlite3 import *
import os
import random
import ipdb
from models.player import Player
from models.game_space import Game_space
from models.game import Game
from models.__init__ import CONN, CURSOR

player_house_positions = [4, 10, 16, 22]
player_home_position = random.sample(player_house_positions, k=4)

def exit_program():
    os.system('clear')
    print("Goodbye!")
    exit()
    
def exit_program_early(game, players, homes):
    for player in players:
        Player.delete(player)
    for home in homes:
        Game_space.delete(home)
    Game.delete(game)
    os.system('clear')
    print("Goodbye!")
    exit()

