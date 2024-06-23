#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import os
import ipdb
import random
from models.player import Player
from models.game import Game
from models.space import Space
from models.game_space import Game_space
from sqlite3 import *


def scratch(game):
    numbers = [0, 1, 2, 3, 4, 5]
    numbers = random.sample(numbers, k=6)
    itchies = {"A": numbers[0], "B": numbers[1], "C": numbers[2], "D": numbers[3], "E": numbers[4], "F": numbers[5]}
    print(f"Your Itchy Ticket\n")
    ticket = "          $ |A| |B| |C| |D| |E| |F| 0\n"
    print(ticket)
    print("Which letter would you like to itch?\n")
    letter1 = input()
    letter1 = letter1.upper()
    ticket2 = ticket.replace(letter1, str(itchies[letter1]))
    print(ticket2)
    print("Which letter would you like to itch?\n")
    letter2 = input()
    letter2 = letter2.upper()
    ticket3 = ticket2.replace(letter2, str(itchies[letter2]))
    print(ticket3)
    prize = [letter for letter in ticket3 if letter.isdigit()]
    prize = int("".join(prize))
    game.curr_player.money += prize
    print(f"You win ${prize}")

scratch()




#ipdb.set_trace()







#os.system("echo 'hello world'")
#os.system("say -v Zarvox 'hello world'")





#Mac OS X voices for using with the ‘say’ command

#You can pick alternate voice profiles with the -v argument.

#You can also use effects tags:

#Having fun with say command

#[[ slnc 5000 ]] : silence for 5s.
#[[volm 0.9]] changes the volume to the indicated level.
#[[volm +0.1]] increases the volume by the indicated level.
#[[rate 150]] changes the speed
#[[pbas 50]] changes the pitch.
#[[ rset ]] resets all these parameters to default
#'word' :quotes also put the emphasis on the word.