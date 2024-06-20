from sqlite3 import *
from models. __init__ import CONN, CURSOR
from models.game_space import Game_space
import ipdb
#CONN = sqlite3.connect('./monopolython.db')
#CURSOR = CONN.cursor()
class Player():
    
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                """ CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT,
                player_type TEXT,
                curr_pos INTEGER,
                money INTEGER,
                net_worth INTEGER,
                game_id INTEGER,
                FOREIGN KEY (game_id) REFERENCES games(id));""")
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
    def create(cls, name, player_type, curr_pos = 1, money = 1800, net_worth = 1800, game_id = None):
        player = cls(name, player_type, curr_pos, money, net_worth, game_id)
        player.save()
        return player
    
    @classmethod
    def instance_from_db(cls, row):
        return cls(
            row[1], 
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[0],)
        

    def __init__(self, name, player_type, curr_pos = 1, money = 1800, net_worth = 1800, game_id = None, id = None):
        self.name = name
        self.player_type = player_type
        self.curr_pos = curr_pos
        self.money = money
        self.net_worth = net_worth
        self.game_id = game_id
        self.id = id
    
    def __repr__(self):
        return f"{self.name}  |  {self.player_type}  |  Money:${self.money}  |  Net Worth:{self.net_worth}"

    def save(self):
        sql = """
            INSERT INTO players (name, player_type, curr_pos, money, net_worth, game_id)
            VALUES (?, ?, ?, ?, ?, ?);
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

    @classmethod
    def delete(cls, player):
        sql = """ DELETE FROM players WHERE id = ?;"""
        CURSOR.execute(sql, (player.id,))
        CONN.commit()
        
    @classmethod
    def get_all_players_by_gameid(cls, game):
            sql = """"SELECT * FROM players WHERE game_id = ?;"""
            rows = CURSOR.execute(sql, (game.id,)).fetchall()
            return [cls.instance_from_db(row) for row in rows]
        
