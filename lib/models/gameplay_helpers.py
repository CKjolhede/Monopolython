#lib/models/gameplay_helpers.py
from sqlite3 import *
import time
import os
import random
import ipdb
from models.space import Space
from models.player import Player
from models.game_space import Game_space
from models.game import Game
from models.__init__ import CONN, CURSOR

def check_num_players(game):
    players = Player.get_all_players_by_gameid(game)
    return len(players)

def header(game):
    print(game)
    print(game.curr_player)
    print('----------------------\n')

def scratch_ticket(game):
    print("ITCHY TICKETS")
    print("You can win up to $500 on every ticket")
    print("Ticket Price is $50")
    print("-----------------------------")
    print(" Under each spot is a number from 0 to 5 ")
    print(" Select two itchy spots to expose your prize")
    print(" EXAMPLE:")
    print("          $ |A| |B| |C| |D| |E| |F| 0")
    print("pick a letter to reviel the number underneath")
    print("          $ |A| |4| |C| |D| |E| |F| 0")
    print("pick another letter to reviel the number underneath")
    print("          $ |A| |4| |C| |D| |2| |F| 0")
    print("          $      4           2      0")
    print("You win $420\n")
    print("Would you like to buy an ITCHY TICKET?")
    print("1 - YES")
    print("2 - NO")
    choice = input()
    if choice == "1":
        os.system('clear')
        header(game)
        scratch(game)
    elif choice == "2":
        os.system('clear')
        header(game)
        print("You chose not to buy a ticket.")
        
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
    
def print_player_order(game_players):
    print("ORDER OF PLAY:")
    for i, player in enumerate(game_players, start=1):
        print(f"{i} - {player}")
        
def set_empty_player_homes(game, slots):
    for slot in slots:
        space = Space.find_space_by_position(slot)
        space.owned = 1
        space.update()
        #Game_space.create(game.id, None, space.id, "Empty House", slot, 0, 0, "player", 0, 0)
        