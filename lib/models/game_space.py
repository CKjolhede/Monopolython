from sqlite3 import *
from models.__init__ import CONN, CURSOR
from models.space import Space

class Game_space:
    
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                """CREATE TABLE IF NOT EXISTS game_spaces (
                id INTEGER PRIMARY KEY,
                game_id INTEGER,
                player_id INTEGER,
                space_id INTEGER,
                street_name TEXT,
                position INTEGER,
                price INTEGER,
                rent INTEGER,
                neighborhood TEXT,
                houses INTEGER,
                monopoly INTEGER,
                FOREIGN KEY (game_id) REFERENCES games(id),
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (space_id) REFERENCES spaces(id));""")
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
    def create(cls, game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly):
        game_space = cls(game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly)
        game_space.save()
        return game_space
    
    def __init__(self, game_id, player_id, space_id, street_name, position, price = 0, rent = 0, neighborhood = None, houses = 0, monopoly = False, id = None):
        space = Space.find_by_space_position(position)
        self.game_id = game_id
        self.player_id = player_id
        self.space_id = space_id
        self.street_name = street_name
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
            INSERT INTO game_spaces (game_id, player_id, space_id, street_name, position, price, rent, neighborhood, houses, monopoly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.game_id, self.player_id, self.space_id, self.street_name, self.position, self.price, self.rent, self.neighborhood, self.houses, self.monopoly))
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
        
    @classmethod    
    def get_all_homes_by_gameid(cls, gameid):
        sql = """ SELECT * FROM game_spaces WHERE game_id = ?;"""
        rows = CURSOR.execute(sql, (gameid, )).fetchall
        return [cls.instance_from_db(row) for row in rows]
        
    @classmethod
    def instance_from_db(cls, row):
        game_space = cls(
            id = row[0],
            game_id = row[1],
            player_id = row[2],
            space_id = row[3],
            street_name = row[4],
            position = [5],
            price = [6],
            rent = [7],
            neighborhood = [8],
            houses = [9],
            monopoly = [10])
        
    @classmethod
    def get_game_space_by_playerid_gameid(cls, game, player):
        sql = """ SELECT * FROM game_spaces WHERE (game_id = ? AND player_id = ?) LIMIT 1;"""
        row = CURSOR.execute(sql, (game.id, player.id)).fetchone()
        return cls.instance_from_db(row) if row else None        