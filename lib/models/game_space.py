from __init__ import CURSOR, CONN
from sqlite3 import IntegrityError
from space import Space
from game import Game
from player import Player
from helper import Helper

class Game_space:
    
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                """CREATE TABLE IN NOT EXISTS game_spaces (
                id INTEGER PRIMARY KEY,
                game_id INTEGER FOREIGN KEY,
                player_id INTEGER FOREIGN KEY,
                street_name TEXT,
                price INTEGER,
                rent INTEGER,
                position INTEGER,
                neighborhood TEXT,
                houses INTEGER
                monopoly BOOLEAN);""")
        except IntegrityError as e:
            return e

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS game_spaces;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, game_id, player_id, street_name, price, rent, position, neighborhood, houses, monopoly):
        game_space = cls(game_id, player_id, street_name, price, rent, position, neighborhood, houses, monopoly)
        game_space.save()
        return game_space
    
    def __init__(self, game_id, position,  id = None):
        space = Space.find_by_space_position(position)
        self.game_id = game_id
        self.player_id = Game.curr_player.id
        self.street_name = space.street_name
        self.price = space.price
        self.rent = space.rent
        self.position = position
        self.neighborhood = space.neighborhood
        self.houses = 0
        self.monopoly = False 
        self.id = id
        
    def __repr__(self):
        return f"<{self.street_name}: Price = {self.price}: Rent = {self.rent}: Neighborhood = {self.neighborhood}: Number of Houses = {self.houses}: Owner = {(self.find_owner_by_playerid(self.player_id)).name}>"
    
    def save(self):
        sql = """
            INSERT INTO game_spaces (game_id, player_id, street_name, price, rent, position, neighborhood, houses, monopoly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.game_id, self.player_id, self.street_name, self.price, self.rent, self.position, self.neighborhood, self.houses, self.monopoly))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    def update(self):
        sql = """
            UPDATE game_spaces
            SET player_id = ?, street_name = ?, rent = ?, houses = ?, monopoly = ?
            WHERE id = ?;
            """
        CURSOR.execute(sql, (self.player_id, self.street_name, self.rent, self.houses, self.monopoly, self.id))
        CONN.commit()
        
    def delete(self):
        sql = """ DELETE FROM game_spaces WHERE id = ?;"""
        CURSOR.execute(self, (self.id,))
        CONN.commit()
        