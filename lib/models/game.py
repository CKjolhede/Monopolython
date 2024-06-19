
from sqlite3 import *
from models.__init__ import CONN, CURSOR

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
    def create(cls, win_condition = 10000, curr_player = None, next_player = None):
        """ Initialize a new Game instance and save the object to the database """
        game = cls()
        game.save()
        return game
    
    def __init__(self, win_condition = 10000, curr_player = None, next_player = None, id = None):
        self.win_condition = win_condition
        self.curr_player = curr_player
        self.next_player = next_player
        self.id = id
        self.players = []

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
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.win_condition, self.curr_player, self.next_player, self.id))
        CONN.commit()

    def delete(self):
        sql = """ DELETE FROM games WHERE id = ? """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    

        
        
        
