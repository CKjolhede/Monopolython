# lib/models/setup_helper.py
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
    

def enter_new_player(game):
    print("Enter Your Player's Name (required)")
    print("Name must be less than 16 characters")
    print("Enter '0' to return to Player Setup")
    name = input()
    if name == "0":
        os.system('clear')
        Menus.player_setup(game)
    elif not 0 < len(name) < 16:
        os.system('clear')
        print("INVALID ENTRY\n")
        enter_new_player(game)
    else:
        os.system('clear')
        create_player_type(game, name)
        
def create_player_type(game, name):
    print(f"{name}, which type of player you would like to be?\n")
    print('1 REALTOR = The REALTOR receives 10 percent of all property purchases')
    print('2 COP = The COP receives $50 from any player occupying the same space')
    print('3 BUILDER = The BUILDER recieves a 20 percent discount on home purchases')
    print('4 PILOT = The PILOT can roll an unlimited number of doubles')
    print('0 Return to Player Setup')
    value = input()
    if value == "1":
        player_type = "REALTOR"
    elif value == "2":
        player_type = "COP"
    elif value == "3":
        player_type = "BUILDER"
    elif value == "4":
        player_type = "PILOT"
    elif value == "0":
        os.system('clear')
        Menus.player_setup(game)
    else:
        os.system('clear')
        print("You must choose from the 4 player types\n")
        time.sleep(2.5)
        create_player_type(game, name)
    set_player(game, name, player_type)

def set_player(game, name, player_type):
        player = Player.create(name, player_type, 0, 1800, 1800, game.id)
        print(f"Good Luck {player.name}!")
        time.sleep(.5)
        position = player_home_position.pop()
        os.system('clear')
        enter_player_home(position, player, game)
        
def enter_player_home(position, player, game):
    print("Each player begins with a home property.\n")
    print(f"{player.name} enter a name for your home's street?")
    street_name = input()
    if len(street_name) == 0:
        os.system('clear')
        print("Street cannot be left blank/n")
        time.sleep(2.5)
        enter_player_home(position, player, game)
    else:
        assign_game_space(game.id, player.id, position, street_name, position, 0, 100, "player", 0, 0, game) 

def assign_game_space(game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly, game):       
    
    home = Game_space.create(game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly)
    print("\n CONGRATULATIONS!  You now own your first property.")
    print(f"You can find {home.street_name} on the {position}th position on the board")
    print("press ENTER to continue")
    input()
    os.system('clear')
    Menus.player_setup(game)
    
def print_players(game):
    players = get_player_list(game)
    if len(players) == 0:
        print("Game has no players yet\n")
        Menus.player_setup(game)    
    print("Players")
    for i, player in enumerate(players, start=1):
        print(f'{i} - {player}')
    return players

def check_num_players(game):
    players = Player.get_all_players_by_gameid(game)
    return len(players)
    
def remove_player(game):
    players = print_players(game)
    print("Enter the number of the player you would like to remove")
    print("0 - Back to Player Setup")
    choice = input()
    value = int(choice) if choice in ["0","1","2","3","4"] else 10
    if value > len(players):
        os.system('clear')
        print("INVALID ENTRY\n")
        time.sleep(1)
        remove_player(game)
    elif value == 0:
        os.system('clear')
        Menus.player_setup(game)
    remove_player_home(game, players[(value - 1)])
    print(f"{players[(value - 1)].name}'s home has been deleted")
    print(f'{players[(value -1)].name} has been deleted')
    Player.delete(players[(value - 1)])
    print("press ENTER to continue")
    input()
    os.system('clear')
    remove_player(game)
    
def remove_player_home(game, player):
    sql = """ SELECT position FROM game_spaces WHERE game_id = ? AND player_id = ?; """
    position = CURSOR.execute(sql, (game.id, player.id)).fetchone()
    player_home_position.append(position[0])
    Game_space.delete(game, player)
    

def edit_player_menu(game):  
    players = print_players(game)
    print("enter the number of the player you would like to EDIT")
    print("0 - Back to Player Setup")
    choice = input()
    value = int(choice) if choice in ["0","1","2","3","4"] else 10
    if value > len(players):
        os.system('clear')
        print("INVALID ENTRY\n")
        time.sleep(1)
        edit_player_menu(game)
    elif value == 0:
        os.system('clear')
        Menus.player_setup(game)
    else:
        player = players[(value - 1)]
        edit_player(game, player)

def edit_player(game, player):
    os.system('clear')
    print(f"Enter {player.name}'s new name")
    print("Name must be less than 16 characters")
    name = input(f'{player.name} will now be called:  ')
    if not 0 < len(name) < 16:
        os.system('clear')
        print("INVALID ENTRY\n")
        edit_player(game, player)
    else:
        os.system('clear')
        player.name = name
    edit_player_type(game, player)

def edit_player_type(game, player): 
    while True:
        print(f"{player.name}, which type of player you would like to be?\n")
        print('1 REALTOR = The REALTOR receives 10 percent of all property purchases')
        print('2 COP = The COP receives $50 from any player occupying the same space')
        print('3 BUILDER = The BUILDER recieves a 20 percent discount on home purchases')
        print('4 PILOT = The PILOT can roll an unlimited number of doubles')
        value = input()
        if value == "1":
            player.player_type = "REALTOR"
            break
        elif value == "2":
            player.player_type = "COP"
            break
        elif value == "3":
            player.player_type = "BUILDER"
            break
        elif value == "4":
            player.player_type = "PILOT"
            break
        else:
            os.system('clear')
            print("You must choose from the 4 player types\n")
            time.sleep(2.5)
    player.update()
    os.system('clear')
    print("Updated Player Info:\n")
    print(player)
    print(" ")
    Menus.player_setup(game)
        

def set_win_condition(game):
    while True:
        try:
                print("enter NET WORTH needed to win")
                print("Must be between 5000 and 20000")
                win_condition = input()
                if not 5000 <= int(win_condition) <= 20000:
                    nope(game)
                else:
                    update_game_win_cond(game, win_condition)
                    Menus.new_game_setup(game)
                    break
        except ValueError:
            continue

def nope(game):
    os.system('clear')
    print("Invalid Entry\n")
    set_win_condition(game)
            

def update_game_win_cond(game, win_condition):
    game.win_condition = int(win_condition)
    game.update()
    print(f'Get to ${game.win_condition} net worth and you will win!')
    time.sleep(1.5)
    os.system('clear')
    Menus.new_game_setup(game)
    
def get_player_list(game):
    return Player.get_all_players_by_gameid(game)

def exit_program_early(game):
    players = get_player_list(game)
    for player in players:
        Game_space.delete(game, player)
        Player.delete(player)
    Game.delete(game)
    os.system('clear')
    print("Goodbye!")
    exit()
    
def exit_program():
    os.system('clear')
    print("Goodbye!")
    exit()
    

    


    
import cli as Menus