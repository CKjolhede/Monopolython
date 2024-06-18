import sqlite3
from sqlite3 import IntegrityError
from models.__init__ import CONN, CURSOR

class Player():
    
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                """CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT,
                player_type TEXT,
                curr_pos INTEGER,
                money INTEGER,
                net_worth INTEGER,
                game_id INTEGER FOREIGN KEY);""")
        except IntegrityError as e:
            return e 

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS players;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, name, player_type, curr_pos = 0, money = 1800, net_worth = 1800, game_id = None):
        player = cls(name, player_type, curr_pos, money, net_worth, game_id)
        player.save()
        return player
    
    @classmethod
    def instance_from_db(cls, row):
        player = cls(
            id = row[0],
            name = row[1], 
            player_type = row[2],
            curr_pos = row[3],
            money = row[4],
            net_worth = row[5],
            game_id = row[6])
        
    @classmethod    
    def get_all_players(cls):
        pass      
        

    def __init__(self, name, player_type, curr_pos = 0, money = 1800, net_worth = 1800, game_id = None, id = None):
        self.name = name
        self.player_type = player_type
        self.curr_pos = curr_pos
        self.money = money
        self.net_worth = net_worth
        self.game_id = game_id
        self.id = id
    
    def __repr__(self):
        return f"<{self.name}: Player Type = {self.player_type}: Money = {self.money}: Net Worth = {self.net_worth}: Postion = {Game_space.find_by_position(self.curr_pos).street_name}>"

    def save(self):
        sql = """
            INSERT INTO players (name, player_type, curr_pos, money, net_worth, game_id)
            VALUES (?, ?, ?, ?, ?, ?};
        """
        CURSOR.execute(sql, (self.name, self.player_type, self.curr_pos, self.money, self.net_worth, self.game_id))
        CONN.commit()
        self.id = CURSOR.lastrowid

    def update(self):
        sql = """
            UPDATE players
            SET name = ?, player_type = ?, curr_pos = ?, money = ?, net_worth = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.name, self.player_type, self.curr_pos, self.money, self.net_worth, self.id))
        CONN.commit()

    def delete(self):
        sql = """ DELETE FROM players WHERE id = ?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        


    #@property
    #def name(self):
    #    return self._name

    #@name.setter
    #def name(self, name):
    #    if not isinstance(name, str):
    #        raise TypeError("Player name must be a string")
    #    elif 0 < len(name) < 16:
    #        raise ValueError("Player name must be less than 16 characters")
    #    else:
    #        self._name = name