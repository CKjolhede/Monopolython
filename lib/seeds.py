from models.__init__ import CONN, CURSOR
from models.game import Game
from models.space import Space
from models.player import Player
from models.game_space import Game_space
from sqlite3 import *




def seed_spaces():
    Space.drop_table()
    spaces = [('GO', 0, 0, 1, "Game", 1),
            ('unowned', 60, 30, 2, "Pink", 0),
            ('unowned', 80, 40, 3, "Pink", 0),
            ('unowned', 0, 100, 4, "Player", 0),
            ('unowned', 100, 50, 5, "Lt Blue", 0),
            ('unowned', 120, 60, 6, "Lt Blue", 0),
            ('CASINO', 0, 0, 0, "Game", 1),
            ('unowned', 140, 70, 8, "Purple", 0),
            ('unowned', 160, 80, 9, "Purple", 0),
            ('unowned', 0, 100, 10, "Player", 0),
            ('unowned', 180, 90, 11, "Orange", 0),
            ('unowned', 200, 100, 12, "Orange", 0),
            ("Free Spasce", 0, 0, 13, "Game", 1),
            ("unowned", 220, 110, 14, "Red", 0),
            ("unowned", 240, 120, 15, "Red", 0),
            ("unowned", 0, 100, 16, "Player", 0),
            ('unowned', 260, 130, 17, "Yellow", 0),
            ("unowned", 280, 140, 18, "Yellow", 0),
            ("Pay HOA", 0, 200, 19, "Game", 1),
            ("unowned", 300, 150, 20, "Green", 0),
            ("unowned", 320, 160, 21, "Green", 0),
            ("unowned", 0, 100, 22, "Player", 0),
            ("unowned", 360, 130, 23, "Blue", 0),
            ("unowned", 400, 200, 24, "Blue", 0)]
    for space in spaces:
        Space.create(*space)
    print("Spaces have successfully seeded")
if __name__ == "__main__":
    
    seed_spaces()