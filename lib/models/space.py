from __init__ import CURSOR, CONN
import sqlite3
from sqlite3 import IntegrityError
from helper import Helper
from game_space import Game_space
from player import Player

CONN = sqlite3.connect('resources.db')
CURSOR = CONN.execute()

class Space(Helper):
        
    @classmethod
    def create_table(cls):
        sql = """(CREATE TABLE IF NOT EXISTS spaces 
        (id = INTEGER PRIMARY KEY,
        street_name TEXT,
        price INTEGER,
        rent INTEGER,
        position = INTEGER,
        neighborhood = TEXT);"""
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = """ DROP TABLE IF EXISTS spaces; """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def create(cls, street_name, price, rent, position, neighborhood):
        space = cls(street_name, price, rent, position, neighborhood)
        space.save()
        return space
    
    @classmethod
    def find_by_space_position(cls, position):
        sql = """ SELECT * FROM space WHERE position = ? LIMIT 1;"""
        row = CURSOR.execute(sql, (position,)).fetchone()
        return cls.instance_from_db(row) if row else None
        
    @classmethod
    def instance_from_db(cls, row):
        return cls(
            id=row[0],
            street_name=row[1],
            price=row[2],
            rent=row[3],
            position=row[4],
            neighborhood=row[5])
    
    def __init__(self, street_name, price, rent, position, neighborhood, id = None):
        self.street_name = street_name
        self.price = price
        self.rent = rent
        self.position = position
        self.neighborhood = neighborhood
        self.id = id
        
    def save(self):
        sql = """INSERT INTO spaces (street_name, price, rent, position, neighborhood)
            VALUES (?, ?, ?, ?); """
        CURSOR.execute(sql (self.street_name, self.price, self.rent, self.position, self.neighborhood))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    def update(self):
        sql = """UPDATE spaces
        SET street_name = ?, price = ?, rent = ?, position = ?, neighborhood = ?
        WHERE id = ?;"""
        CURSOR.execute(sql, (self.street_name, self.price, self.rent, self.position, self.neighborhood))
        CONN.commit()
        
    def delete(self):
        sql = """ DELETE FROM spaces WHERE id = ?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    def __repr__(self):
        return f"<{self.street_name}: Price = {self.price}: Rent = {self.rent}: Neighborhood = {self.neighborhood}>"