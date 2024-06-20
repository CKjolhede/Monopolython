# lib/cli.py
import time
from sqlite3 import *
import os
import random
import ipdb
from models.player import Player
from models.game_space import Game_space
from models.game import Game
from models.__init__ import CONN, CURSOR



os.system('clear')


    
def main_menu():
    print("WELCOME TO MONOPOLYTHON!")
    print("Please select an option:")
    print("1 Start New Game")
    print("2 Load Saved Game - COMING SOON!")
    print("3 Exit Game")
        
def main():
    while True:
        main_menu()
        print("Enter the number of your choice:")
        choice = input("")
        if choice == "1":
            game = Game.create()
            os.system('clear')
            new_game_setup(game)
        elif choice == "2":      
            print("\nThis feature is not yet available\n")
            time.sleep(1.5)
        elif choice == "3":
            exit_program()
        else:
            os.system('clear')
            print("Invalid selection\n")


def new_game_setup_menu():
    print("New Game Menu:")
    print("1 Add / Remove Players")
    print("2 Change $ amount to win")
    print("3 Start Game")
    print("4 Quit Game")
    
def new_game_setup(game):
    new_game_setup_menu()
    choice = input()
    if choice == "1":
        os.system('clear')
        player_setup(game)
    elif choice == "2":
        os.system('clear')
        set_win_condition(game)
    elif choice == "3":
        os.system('clear')
        start_game(game)
    elif choice == "4":
        exit_program_early(game)
    else:
        os.system('clear')
        print("That is not a valid input.")
        print("Enter the number next to your choice.\n")
        time.sleep(1)
        new_game_setup(game)
    
    
def player_setup_menu():
    print("Player Setup Menu")
    print("1 Add Player")
    print("2 See All Players")
    print("3 Remove Player")
    print("4 Edit Player")
    print("5 Return to Game Setup")
    print("6 Quit Game")
    
def player_setup(game):
    player_setup_menu()
    print("What would you like to do?")
    choice = input()    
    if choice == "1":
        os.system('clear')
        if len(player_home_position) != 0:
            enter_new_player(game)
        else:
            print("Max number of players reached")
            player_setup(game)
    elif choice == "2":
        os.system('clear')
        print_players(game)
        player_setup(game)
    elif choice == "3":
        os.system('clear')
        remove_player(game)
    elif choice == "4":
        os.system('clear')
        edit_player_menu(game)
    elif choice == "5":
        os.system('clear')
        new_game_setup(game)
    elif choice == "6":
        os.system('clear')
        exit_program_early(game)
    else:
        os.system('clear')
        print("Invalid choice, please select again")
        time.sleep(2.5)
        player_setup(game)
        
def game_play_menu(game):
    print("Game Menu")
    print("1 BUY HOUSES")
    print("2 ROLL DICE")
    print("3 SKIP TURN (COSTS $100)")
    print("4 QUIT GAME")
    
def game_play(game):
    game_play_menu(game)
    choice = input()
    if choice == "1":
        os.system('clear')
        buy_houses(game)
    elif choice == "2":
        os.system('clear')
        roll(game)
    elif choice == "3":
        os.system('clear')
        skip_turn(game)
    elif choice == "4":
        os.system('clear')
        exit_program(game)
    else:
        os.system('clear')
        print("Invalid choice, please select again")
        time.sleep(2.5)
        game_play(game)

from models.gameplay_helpers import (start_game, game_players, t, doubles_count, buy_houses, roll, skip_turn)

from models.setup_helper import (enter_new_player, player_home_position, print_players, remove_player, edit_player_menu, set_win_condition, exit_program, exit_program_early,  )
if __name__ == "__main__":
    main()