import sqlite3
from sqlite3 import *
from models.helper import Helper
from models.__init__ import CONN, CURSOR

class Game():

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Game instances """
        try:
            with CONN:
                CURSOR.execute(
                """CREATE TABLE IF NOT EXISTS games (
                win_condition INTEGER,
                curr_player TEXT,
                next_player TEXT);""")
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
    def create(cls, win_condition = 10000):
        """ Initialize a new Game instance and save the object to the database """
        game = cls(win_condition)
        game.save()
        return game
    
    def __init__(self, win_condition, id = None):
        self.win_condition = win_condition
        self.players = []
        self.curr_player = ""
        self.next_player = ""
        self.id = id

    def __repr__(self):
        return f"<Game {self.id}: First Net-Worth = {self.win_condition} wins: List of players: {self.players}>"
    
    def save(self):
        sql = """
            INSERT INTO games (win_condition, curr_player, next_player)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.win_condition, self.curr_player, self.next_player))
        CONN.commit()
        self.id = CURSOR.lastrowid

    def update(self):
        sql = """
            UPDATE games
            SET win_condition = ?, curr_player = ?, next_player = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.win_condition, self.curr_player, self.next_player, self.id))
        CONN.commit()

    def delete(self):
        sql = """ DELETE FROM games WHERE id = ? """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

Game.drop_table()      
Game.create_table()  
#@property
    #def win_condition(self):
    #    return self._win_condtion

    #@win_condition.setter
    #def win_condition(self, win_condition):
    #    if not isinstance(win_condition, int):
    #        raise TypeError("Win Condition must be an integer")
    #    elif 5000 < self.win_condition < 20000:
    #        raise ValueError("Dollar amount must be between 5000 and 20000")
    #    else:
    #        self._win_condition = win_condition