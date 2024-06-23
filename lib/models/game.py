
from sqlite3 import *
from models.__init__ import CONN, CURSOR
import ipdb

class Game():

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Game instances """
        try:
            with CONN:
                CURSOR.execute(
                """CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                win_condition INTEGER,
                curr_player TEXT);""")
        except IntegrityError as e:
            return e 

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Game instances """
        sql = """
            DROP TABLE IF EXISTS games;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, win_condition = 10000, curr_player = None):
        """ Initialize a new Game instance and save the object to the database """
        game = cls()
        game.save()
        return game
    
    def __init__(self, win_condition = 10000, curr_player = None, id = None):
        self.win_condition = win_condition
        self.curr_player = curr_player
        self.id = id

    def __repr__(self):
        return f"Current Player: {self.curr_player.name}"
    
    def save(self):
        sql = """
            INSERT INTO games (win_condition, curr_player)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.win_condition, self.curr_player))
        CONN.commit()
        self.id = CURSOR.lastrowid

    def update(self):
        sql = """
            UPDATE games SET win_condition = ?, curr_player = ? WHERE id = ?;
        """
        #ipdb.set_trace()
        CURSOR.execute(sql, (self.win_condition, self.curr_player.name, self.id,))
        CONN.commit()
        return self
    
    @classmethod
    def delete(cls, game):
        sql = """ DELETE FROM games WHERE id = ?;"""
        CURSOR.execute(sql, (game.id,))
        CONN.commit()
        
    

        
        
        
