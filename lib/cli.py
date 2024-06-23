# lib/cli.py
import time
from sqlite3 import *
import os
import random
from models.setup_helper import (seed_spaces)
from models.gameplay_helpers import (scratch_ticket, header, print_player_order, set_empty_player_homes)
import ipdb
from models.player import Player
from models.space import Space
from models.game_space import Game_space
from models.game import Game
from models.__init__ import CONN, CURSOR
    
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
            os.system('clear')    
            print("\nThis feature is not yet available\n")
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
    print("6 Start Game")
    print("7 Quit Game")
    
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
        start_game(game)
    elif choice == "7":
        os.system('clear')
        exit_program_early(game)
    else:
        os.system('clear')
        print("Invalid choice, please select again\n")
        player_setup(game)
        

def enter_new_player(game):
    print("Enter Your Player's Name (required)")
    print("Name must be less than 16 characters")
    print("Enter '0' to return to Player Setup")
    name = input()
    os.system('clear')
    if len(name) >= 16 or not name.isalpha():
        if name == "0":
            player_setup(game)
        else:
            print("INVALID ENTRY\n")
            enter_new_player(game)
    else:
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
        player_setup(game)
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
    if not street_name.isalpha():
        os.system('clear')
        print("Street cannot be left blank\n")
        enter_player_home(position, player, game)
    else:
        assign_game_space(game.id, player.id, position, street_name, position, 0, 100, "player", 0, 0, game) 

def assign_game_space(game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly, game):       
    space = Space.find_space_by_position(position)
    space.owned = 1
    space.update()
    home = Game_space.create(game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly)
    print("\n CONGRATULATIONS!  You now own your first property.")
    print(f"You can find {home.street_name} on the {position}th position on the board")
    print("press ENTER to continue")
    input()
    os.system('clear')
    player_setup(game)
    
def print_players(game):
    players = Player.get_all_players_by_gameid(game.id)
    if len(players) == 0:
        print("Game has no players yet\n")
        player_setup(game)    
    print("Players")
    for i, player in enumerate(players, start=1):
        print(f'{i} - {player}')
    return players
    
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
        player_setup(game)
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
    space = Space.find_space_by_position(position[0])
    space.owned = 0
    space.update()
    
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
        player_setup(game)
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
    player_setup(game)
        

def set_win_condition(game):
    print("enter NET WORTH needed to win")
    print("Must be between 5000 and 20000")
    win_condition = input()
    if win_condition != 5000 <= int(win_condition) <= 20000 or win_condition.isdigit():
        os.system('clear')
        print("Invalid Entry\n")
        set_win_condition(game)
    else:
        update_game_win_cond(game, win_condition)
        new_game_setup(game)

def update_game_win_cond(game, win_condition):
    game.win_condition = int(win_condition)
    game.update()
    os.system('clear')
    print(f'Get to ${game.win_condition} net worth and you will win!')
    new_game_setup(game)
    
def exit_program_early(game):
    players = Player.get_all_players_by_gameid(game.id)
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

def start_game(game):
    global game_players
    global player_home_position    
    set_empty_player_homes(game, player_home_position)
    gamers = Player.get_all_players_by_gameid(game.id)
    game_players = random.sample(gamers, k=len(gamers))
    game.curr_player = game_players[0]
    game.update()
    os.system('clear')
    game_play(game)
    
def set_current_player(game):
    global t
    turn = t % len(game_players)
    game.curr_player = game_players[(turn)]
    game.update()
    return game.curr_player

def game_play_menu(game):
    header(game)
    print("\n Game Menu")
    print("1 BUY HOUSES")
    print("2 ROLL DICE")
    print("3 SKIP TURN (COSTS $100)")
    print("4 QUIT GAME")
    
def game_play(game):
    global t
    global game_players
    if t == 0:
        print_player_order(game_players)
    game_play_menu(game)
    choice = input()
    if choice == "1":
        os.system('clear')
        header(game)
        buy_houses(game)
    elif choice == "2":
        os.system('clear')
        header(game)
        roll(game)
    elif choice == "3":
        os.system('clear')
        header(game)
        skip_turn(game)
    elif choice == "4":
        os.system('clear')
        exit_program()
    else:
        os.system('clear')
        print("Invalid choice, please select again")
        game_play(game)

def roll(game):
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    print(f"{game.curr_player.name} is on space {game.curr_player.curr_pos}")
    print('_______  _______')
    print(f'|_{die1}_|  |_{die2}_|')
    dice = (die1 + die2)
    print(f"{game.curr_player.name}, you rolled a {dice}")
    global doubles_count
    global t
    if die1 == die2:
        doubles_count += 1
        print("DOUBLES!")
        if doubles_count <= 2 or game.curr_player.player_type == "PILOT":
            print("You get to roll again after this turn.")
            t -= 1
            move(game, dice) 
        else:
            print(f"{game.curr_player.name}, that was your 3rd double, you do not move and your turn ends.")
            doubles_count = 0
            end_turn(game)
    else:
        doubles_count = 0
        move(game, dice)
            
def move(game, dice):
    header(game)
    moveto = game.curr_player.curr_pos + dice
    if moveto > 24:
        pass_go(game, moveto)    
    else: 
        game.curr_player.curr_pos = moveto  
    space = Space.find_space_by_position(game.curr_player.curr_pos)
    print(f"{game.curr_player.name} landed on {space.street_name}")
    speedtrap(game)
    if space.owned == 0 and space.position not in player_house_positions:
        os.system('clear')
        header(game)
        buy_property(game, space)
    elif space.position in player_house_positions:
        print("This property is an empty player home and cannot be purchased.")
    elif space.owned == 1:
        game_space = Game_space.find_gamespace_by_position(game.id, game.curr_player.curr_pos)
        owner = Player.find_by_id(game_space.player_id)
        if owner.id == game.curr_player.id:
            print("You own this property.")
        else:
            game.curr_player.money -= game_space.rent
            owner.money += game_space.rent
            print(f"\nYou pay {owner.name} ${game_space.rent} for rent.")
    elif space.position == 7:
        os.system('clear')
        header(game)
        casino(game)
    elif space.position == 13:
        os.system('clear')
        header(game)
        scratch_ticket(game)
    elif space.position == 19:
        os.system('clear')
        header(game)
        pay_taxes(game)
    elif space.position == 1:
        os.system('clear')
        header(game)
        print("You safely land on GO")
    else:
        input("something is wrong")
    end_turn(game)
        
    
def pay_taxes(game):
    pass
        
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
        game_play(game)  
    else:
        os.system('clear')
        print("Invalid choice, please select again.")
        buy_houses(game)

def skip_turn(game):
    print(f"{game.curr_player.name}, you are skipping your turn.")
    print("You pay $100 to the bank.")
    game.curr_player.money -= 100
    end_turn(game)

def casino(game):  # sourcery skip: remove-redundant-if
    print("Go into the Casino? Y or N")
    value = input()
    if value == "Y" or "y":
        os.system('clear')
        casinogame(game)
    elif value == "N" or "n":
        os.system('clear')
        print("You chose not to enter the Casino.")
    else:
        os.system('clear')
        print("Invalid choice, please select again.")
        casino(game)
        
def casinogame(game):
    print("Welcome to the Casino!")
    print(f'You have ${game.curr_player.money}')
    print("Place your bet.\nRoll an even number to win double your bet.\nRoll an odd number and you lose your bet.")
    print("How much would you like to bet?")
    print("Enter 0 to Leave Casino")
    bet = input()
    if int(bet) == 0:
        os.system('clear')
        end_turn(game)
    elif int(bet) > game.curr_player.money or not bet.isdigit():
        os.system('clear')
        print("Invalid bet, please try again.")
        casinogame(game)
    print(f'You have bet ${bet}')
    game.curr_player.money -= int(bet)
    input("Press ENTER to roll the dice")
    roll = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    print(f'|{roll}| |{roll2}|')
    print(f'\nYou rolled a {roll + roll2}')
    if (roll + roll2) % 2 == 0:
        print(f'YOU WIN ${int(bet) * 2}!')
        game.curr_player.money += (int(bet) * 2)
    else:
        print(f'YOU LOST ${int(bet)}')
        game.curr_player.money -= int(bet)
    print(f'You now have ${game.curr_player.money}')
    input("Press ENTER to end turn")
    os.system('clear')

def buy_property(game, space):
    neighborhood_props_owned = Player.player_props_by_neighborhood(game.id, game.curr_player.id, space.neighborhood)
    print(f"{game.curr_player.name} would you like to buy this property?")
    print(f"Price: ${space.price}")
    print(f"Rent: ${space.rent}")
    print(f"Neighborhood: {space.neighborhood}")
    print(" ------------------------------ ")
    print(f"You have ${game.curr_player.money}")
    print(f"You own {len(neighborhood_props_owned)} other properties in this neighborhood.")
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
    
def name_property(game):
    print(f"{game.curr_player.name}, what would you like to name this property?")
    street_name = input()
    if not 0 < len(street_name) < 20:
        print("Street name must be between 1 and 20 characters. Please try again.")
        name_property(game)
    else:
        print(f"{street_name} is now the name of this property.")
        return street_name
    
def pass_go(game, moveto):
    game.curr_player.curr_pos = moveto - 24
    game.curr_player.money += 200
    print(f"{game.curr_player.name} has passed GO!")
    print(f"{game.curr_player.name} collects $200")
    game.curr_player.update()
    return

def monopoly_check(game, space):
    neighborhood_props = Player.player_props_by_neighborhood(game.id, game.curr_player.id, space.neighborhood)
    if len(neighborhood_props) == 2:
        print(f"{game.curr_player.name} now has a monopoly in the {space.neighborhood} neighborhood.")
        print("Rent for all properties in this neighborhood is now doubled.")
        for prop in neighborhood_props:
            prop.rent = (prop.rent * 2)
            prop.update()

def speedtrap(game):
    global game_players
    for player in game_players:
        if player.curr_pos == game.curr_player.curr_pos and player.id != game.curr_player.id and player.player_type == "COP":
            print(f"{player.name} is a COP and has caught you speeding!")
            input(f"Press enter to pay {player.name} $100")
            game.curr_player.money -= 100
            player.money += 100
            player.update()

def pay_realtors(price):
    global game_players
    for player in game_players:
        if player.player_type == "REALTOR":
            print(f"{player.name} is a REALTOR and has earned {price * 0.1} for this sale.")
            player.money += (price * 0.1)
            player.update()

def end_turn(game):
    global t
    t += 1
    game.curr_player.update
    game.curr_player.networth = calc_net_worth(game)
    game.curr_player.update()
    check_win(game)
    set_current_player(game)
    game.update()
    game_play(game)

def calc_net_worth(game):
    props = Game_space.get_all_player_props(game.id, game.curr_player.id)
    propvalue = sum(
        (prop.houses * prop.price / 4) + (prop.price / 2) for prop in props
    )
    return game.curr_player.money + propvalue
    
def check_win(game):
    if game.curr_player.net_worth > game.win_condition:
        os.system('clear')
        print(f'{game.curr_player} has won the game!')
        input("Press ENTER to exit")
        

if __name__ == "__main__":
    seed_spaces()
    player_house_positions = [4, 10, 16, 22]
    player_home_position = random.sample(player_house_positions, k=4)    
    game_players = []
    t = len(game_players)
    doubles_count = 0
    os.system('clear')   
    main()