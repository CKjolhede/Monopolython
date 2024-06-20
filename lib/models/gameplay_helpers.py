#lib/models/gameplay_helpers.py
import time
from sqlite3 import *
import os
import random
import ipdb
from models.space import Space
from models.player import Player
from models.game_space import Game_space
from models.game import Game
from models.__init__ import CONN, CURSOR

game_players = []
t = len(game_players)
doubles_count = 0

#def set_player_order(game):
#    gamers = Player.get_all_players_by_gameid(game.id)
#    players = random.sample(gamers, k=len(gamers))
    
#    print("Player Order:")
#    for i in range(len(players)):
#        print(f"{i} - {players[(i - 1)].name}")
#    game_players.append = players
#    return players

def start_game(game):
    #set_player_order(game)
    gamers = Player.get_all_players_by_gameid(game.id)
    players = random.sample(gamers, k=len(gamers))
    game_players.append = players
    game.curr_player = players[0]
    game.next_player = players[1]
    game.update(game)
    Menus.game_play(game)
    
def set_current_player(game):
    turn = t % len(game_players)
    game.curr_player = game_players[(turn)]
    game.next_player = game_players[(turn + 1)]
    game.update()
    return game.curr_player

def buy_houses(game):
    props = Game_space.get_all_player_props_by_monopoly(game)
    i = 0
    for prop in props:
        if game.curr_player.player_type == "BUILDER":
            print(f'{i + 1} - {prop.street_name} houses cost ${prop.rent * .4}')
        else:
            print(f'{i + 1} - {prop.street_name} houses cost ${prop.rent * .5}')
    print("\n Onto which property would you like to build a house?")
    print("0 - Return to Main Menu")
    choice = input()
    if 0 < int(choice) < (len(props) + 1) and choice.isdigit():
        prop = props[(int(choice) - 1)]
        prop.houses += 1
        if game.curr_player.player_type == "BUILDER":
            game.curr_player.money -= prop.price * .4
        else:   
            game.curr_player.money -= prop.price * .5
        game.curr_player.update()
        prop.update()
    elif choice == "0":
        os.system('clear')
        Menus.game_play(game)  
    else:
        os.system('clear')
        print("Invalid choice, please select again.")
        buy_houses(game)

def skip_turn(game):
    print(f"{game.curr_player.name}, you are skipping your turn.")
    print("You pay $100 to the bank.")
    game.curr_player.money -= 100
    end_turn(game)

def roll(game):
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    print(f'|{die1}|  |{die2}|')
    dice = (die1 + die2)
    print(f"{game.curr_player.name}, you rolled a {dice}")
    if die1 == die2:
        doubles_count += 1
        print("DOUBLES!")
        if doubles_count <= 2 or game.curr_player.player_type == "PILOT":
            print("You get to roll again after this turn.")
            turn -= 1
            move(game, dice) 
        else:
            print(f"{game.curr_player.name}, that was your 3rd double, you do not move and your turn ends.")
            doubles_count = 0
            end_turn(game)
    else:
        doubles_count = 0
        move(game, dice)
        
def move(game, dice):
    game.curr_player.position += dice
    space = Space.find_space_by_position(game.curr_player.position)
    print(f"{game.curr_player.name} landed on {space.street_name}")
    if space.owned == 0:
        buy_property(game, space)
    elif space.owned == 1:
        game_space = Game_space.find_space_by_position(game, game.curr_player.position)
        owner = Player.find_by_id(game_space.player_id)
        print(f"You pay {owner.name} ${game_space.rent} for rent.")
    speedtrap(game)
    end_turn(game)
    
def buy_property(game, space):
    neighborhood_props_owned = count_of_prop_by_neighborhood(game.id, game.curr_player.id, space.neighborhood)
    print(f"{game.curr_player.name} would you like to buy this property?")
    print(f"Price: ${space.price}")
    print(f"Rent: ${space.rent}")
    print(f"Neighborhood: {space.neighborhood}")
    print(" ------------------------------ ")
    print(f"You have ${game.curr_player.money}")
    print(f"You own {neighborhood_props_owned} other properties in this neighborhood.")
    print("1 - YES")
    print("2 - NO")
    choice = input()
    if choice == "1":
        closing(game, space)
    elif choice == "2":
        print("You chose not to buy this property.")
    else:
        os.system('clear')
        print("Invalid choice, please select again.")
        buy_property(game, space)
        
def closing(game, space):
    game.curr_player.money -= space.price
    pay_realtors(space.price)
    street_name = name_property(game)
    prop = Game_space.create(
        game.id, 
        game.curr_player.id, 
        space.id, 
        street_name,
        space.position, 
        space.price, 
        space.rent, 
        space.neighborhood, 
        0, 
        0)
    space.owned = 1
    space.update()
    game.curr_player.update()
    monopoly_check(game, prop)
    print(f"Congratulations! You now own {prop.street_name}")
    end_turn(game)
    
def name_property(game):
    print(f"{game.curr_player.name}, what would you like to name this property?")
    street_name = input()
    if not 0 < len(street_name) < 20:
        print("Street name must be between 1 and 20 characters. Please try again.")
        name_property(game)
    else:
        print(f"{street_name} is now the name of this property.")
        return street_name
    
def monopoly_check(game, space):
    neighborhood_props = count_of_prop_by_neighborhood(game.id, game.curr_player.id, space.neighborhood)
    if len(neighborhood_props) == 2:
        print(f"{game.curr_player.name} now has a monopoly in the {space.neighborhood} neighborhood.")
        print("Rent for all properties in this neighborhood is now doubled.")
        props = Game_space.get_all_props_by_neighborhood(game.id, space.neighborhood)
        for prop in props:
            prop.rent = (prop.rent * 2)
            prop.update()
            print(f'Rent for {prop.street_name} is now ${prop.rent}')

def count_of_prop_by_neighborhood(game_id, player_id, neighborhood):
    sql = """ SELECT COUNT(*) FROM game_spaces WHERE game_id = ? AND player_id = ? AND neighborhood = ?;"""
    return CURSOR.execute(sql, (game_id, player_id, neighborhood))

def speedtrap(game):
    for player in game_players:
        if player.position == game.curr_player.position and player.id != game.curr_player.id and player.player_type == "COP":
            print(f"{player.name} is a COP and has caught you speeding!")
            print("You pay the COP $100")
            game.curr_player.money -= 100
            player.money += 100
            game.curr_player.update()
            player.update()
            return

def pay_realtors(price):
    for player in game_players:
        if player.player_type == "REALTOR":
            print(f"{player.name} is a REALTOR and has earned {price * 0.1} for this sale.")
            player.money += (price * 0.1)
            player.update()
            return

def end_turn(game):
    t += 1
    game.curr_player.update()
    calc_net_worth(game)
    check_win(game)
    game.curr_player.update()
    set_current_player(game)
    game.update()
    Menus.game_play(game)

def calc_net_worth(game):
    props = Game_space.get_all_player_props(game, game.curr_player)
    game.curr_player.networth = game.curr_player.money + sum((prop.houses * prop.price * .25) + (prop.price * .5) for prop in props)
    return game.curr_player.net_worth
    
def check_win(game):
    if calc_net_worth(game) < game.win_condition:
        return
    os.system('clear')
    print(f'{game.curr_player} has won the game!')
    print("Press ENTER to exit")
    input()

import cli as Menus