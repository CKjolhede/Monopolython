# lib/cli.py
import sqlite3
import rich
import pick
import os
import random
from models.player import Player
from models.game_space import Game_space
from models.game import Game
from models.helper import Helper
from models.__init__ import CONN, CURSOR

player_house_positions = [3, 9, 15, 21]
player_home_position = random.sample(player_house_positions, k=4)



def main_menu():
    print("Please select an option:")
    print("1 Start New Game")
    print("2 Exit Game")

def exit_program():
        print("Goodbye!")
        exit()
        
def main():
    while True:
        main_menu()
        choice = input("What would you like to do?\n Enter the number of your choice")
        if choice == "1":
            game = Game.create()
            new_game_setup(game)
        elif choice == "2":
            exit_program()
        else:
            print("Invalid choice")


def new_game_setup_menu():
    print("New Game Menu:")
    print("1 Add / Remove Players")
    print("2 Change $ amount to win")
    print("3 Start Game")
    print("4 Quit Game")
    
def new_game_setup(game):
        os.system('clear')
        new_game_setup_menu()
        choice = input()
        if choice == "1":
            player_setup(game)
        elif choice == "2":
            print("Enter net worth needed to win")
            print("Must be between 5000 and 20000")
            game.win_condition == input(10000)
            game.update()
        elif choice == "3":
            start_game(game)
        elif choice == "4":
            exit_program_prestart(game)
        else:
            print("That is not a valid input.")
            print("Enter the number next to your choice")
    
    
def player_setup_menu():
    print("Players")
    print("1 Add Player")
    print("2 See All Players")
    print("3 Remove Player")
    print("4 Edit Player")
    print("5 Return to Game Setup")
    print("6 Quit Game")
    
def player_setup(game):
    os.system('clear')
    player_setup_menu()
    print("What would you like to do?")
    choice = input()    
    if choice == "1":
        enter_new_player(game)
    elif choice == "2":
        get_all_players_by_game(game)
    elif choice == "3":
        remove_player(game)
    elif choice == "4":
        edit_player(game)
    elif choice == "5":
        new_game_setup(game)
    else:
        print("Invalid choice, please select again")
        
def enter_new_player(game):
        os.system('clear')
        print("Enter Your Player's Name (required)")
        print("Name must be less than 16 characters")
        value = input()
        name = value
        #print(f'my name is {name}')
        if not 0 < len(name) < 16:
            print("Name is invalid")
        else:
        

        print("\n, \n, \n, \n, \n")
        print("Enter which type of player you would like to be")
        print('1 REALTOR = The REALTOR receives 10 percent of all property purchases')
        print('2 COP = The COP receives $50 from any player occupying the same space')
        print('3 BUILDER = The BUILDER recieves a 20 percent discount on home purchases')
        print('4 PILOT = The PILOT can roll an unlimited number of doubles')
        value = input()
        if value == "1":
            player_type = "REALTOR"
        elif value == "2":
            player_type = "COP"
        elif value == "3":
            player_type = "BUILDER"
        elif value == "4":
            player_type = "PILOT"
        else:
            print("You must choose from the 4 player types")
        player = Player.create(name, player_type, 0, 1800, 1800, game.id)
        position = player_home_position.pop
        enter_player_home(position, player, game)
        
def enter_player_home(position, player, game):
        print("\n, \n, \n, \n, \n")
        print("Each player begins with a home property")
        print("What is your home's street name?")
        street_name = input()
        if len(street_name) == 0:
            print("Street cannot be left blank")
        
        Game_space(game.id, player.id, street_name, 0, 100, position, None, 0, False)
        player_setup(game)


    

def get_all_players_by_game(cls, game):
    sql = """ SELECT * FROM players WHERE game_id = game.id """

def start_game(game):
    pass

def exit_program_prestart(game):
    pass

def remove_player(game):
    pass

def edit_player(game):
    pass

if __name__ == "__main__":
    main()