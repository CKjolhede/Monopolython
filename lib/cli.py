# lib/cli.py
import time
from sqlite3 import *
import os
import random
from models.player import Player
from models.game_space import Game_space
from models.game import Game
from models.__init__ import CONN, CURSOR


player_house_positions = [4, 10, 16, 22]
player_home_position = random.sample(player_house_positions, k=4)
os.system('clear')
def main_menu():
    print("WELCOME TO MONOPOLYTHON!")
    print("Please select an option:")
    print("1 Start New Game")
    print("2 Exit Game")

        
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
            exit_program()
        else:
            os.system('clear')
            print("Invalid choice\n")
            time.sleep(2.5)
            main()

def exit_program():
        os.system('clear')
        print("Goodbye!")
        exit()

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
            exit_program()
        else:
            os.system('clear')
            print("That is not a valid input.")
            print("Enter the number next to your choice.\n")
            time.sleep(2.5)
            new_game_setup(game)
    
    
def player_setup_menu():
    print("Players")
    print("1 Add Player")
    print("2 See All Players")
    print("3 Remove Player")   #add home position back into list
    print("4 Edit Player")
    print("5 Return to Game Setup")
    print("6 Quit Game")
    
def player_setup(game):
    players = Player.get_all_players_by_gameid(game.id)
    player_setup_menu()
    print("What would you like to do?")
    choice = input()    
    if choice == "1":
        os.system('clear')
        enter_new_player(game)
    elif choice == "2":
        os.system('clear')
        ipdb.set_trace()
        for player in players:
            print(player.name)        
        player_setup(game)
    elif choice == "3":
        os.system('clear')
        remove_player(game, players)
        player_setup(game)
    elif choice == "4":
        os.system('clear')
        edit_player(game)
    elif choice == "5":
        os.system('clear')
        new_game_setup(game)
    elif choice == "6":
        players = Player.get_all_players_by_gameid(game.id)
        homes = Game_space.get_all_homes_by_gameid(game.id)
        os.system('clear')
        exit_program_prestart(game, players, homes)
    else:
        os.system('clear')
        print("Invalid choice, please select again")
        time.sleep(2.5)
        player_setup(game)
        
def remove_player(game, players):
    os.system('clear')
    for player in players:
        print(f'{player.index} - {player.name}')
    print("Enter number next to the player you would like to remove")
    value = input()
    if value >= len(players):
        os.system('clear')
        print("Invalid entry")
        time.sleep(2.5)
        remove_player(game, players)
    remove_player_home(game, player[value])
    print(f"{player[value].name}'s home has been deleted")
    Player.delete(player[value])
    print(f'{player[value].name} has been deleted')
        

def remove_player_home(player, game):
        home = Game_space.get_game_space_by_playerid_gameid(game, player)
        Game_space.delete(home)
        

        
def enter_new_player(game):
        print("Enter Your Player's Name (required)")
        print("Name must be less than 16 characters")
        name = input()
        if not 0 < len(name) < 16:
            os.system('clear')
            print("Name is invalid")
            enter_new_player(game)
        else:
            os.system('clear')
            create_player_type(game, name)
        
def create_player_type(game, name):
        print(f"{name}, which type of player you would like to be?")
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
            os.system('clear')
            print("You must choose from the 4 player types\n")
            time.sleep(2.5)
            create_player_type(game,name)
            
        player = Player.create(name, player_type, 0, 1800, 1800, game.id)
        print(f"Good Luck {player.name}!")
        time.sleep(2)
        position = player_home_position.pop()
        os.system('clear')
        enter_player_home(position, player, game)
        
def enter_player_home(position, player, game):
        print("Each player begins with a home property")
        print(f"{player.name} enter a name for your home's street?")
        street_name = input()
        if len(street_name) == 0:
            os.system('clear')
            print("Street cannot be left blank")
            time.sleep(2.5)
            enter_player_home(position, player, game)
        else:
            assign_game_space(game.id, player.id, position, street_name, 0, 100, position, None, 0, 0, game, player) 

def assign_game_space(game_id, player_id, space_id, street_name, price, rent, position, neighborhood, houses, monopoly, game, player):       
            Game_space.create(game_id, player_id, space_id, street_name, price, rent, position, neighborhood, houses, monopoly)
            print("\n \n CONGRATULATIONS!  You now own your first property.")
            print(f"You can find your home on the {position}th position on the board")
            time.sleep(2.5)
            os.system('clear')
            player_setup(game)

def set_win_condition(game):
        print("Enter net worth needed to win")
        print("Must be between 5000 and 20000")
        win_condition = input()
        if not 5000 <= int(win_condition) <= 20000:
            print("Invalid entry")
            time.sleep(2.5)
            set_win_condition(game)
        else:
            update_game_win_cond(game, win_condition)

def update_game_win_cond(game, win_condition):
    game.win_condition = int(win_condition)
    game.update()
    print(f'Get to ${win_condition} net worth and you will win!')
    time.sleep(2.5)
    os.system('clear')
    new_game_setup(game)
    
def start_game(game):
    pass

def exit_program_prestart(game):
    pass

def edit_player(game):
    pass

if __name__ == "__main__":
    main()