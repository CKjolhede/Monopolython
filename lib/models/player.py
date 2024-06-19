from sqlite3 import *
from models.__init__ import CONN, CURSOR
from models.game_space import Game_space

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
        

    def __init__(self, name, player_type, curr_pos = 0, money = 1800, net_worth = 1800, game_id = None, id = None):
        self.name = name
        self.player_type = player_type
        self.curr_pos = curr_pos
        self.money = money
        self.net_worth = net_worth
        self.game_id = game_id
        self.id = id
    
    def __repr__(self):
        return f"<{self.name}: ID# = {self.id}\nPlayer Type = {self.player_type}\nMoney = {self.money}\nNet Worth = {self.net_worth}\n Postion = {self.curr_pos}>"

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

    def delete(self):
        sql = """ DELETE FROM players WHERE id = ?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    @classmethod
    def get_all_players_by_gameid(cls, gameid):
        sql = """ SELECT * FROM players WHERE game_id = ?; """
        rows = CURSOR.execute(sql, (gameid,)).fetchall()
        players = [cls.instance_from_db(row) for row in rows]
        [print(player) for player in players]
        return players