from sqlite3 import *
from models.__init__ import CONN, CURSOR

class Space():
        
    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS spaces 
        (id INTEGER PRIMARY KEY,
        street_name TEXT,
        price INTEGER,
        rent INTEGER,
        position INTEGER,
        neighborhood TEXT,
        owned INTEGER);"""
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = """ DROP TABLE IF EXISTS spaces; """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def create(cls, street_name, price, rent, position, neighborhood, owned):
        space = cls(street_name, price, rent, position, neighborhood, owned)
        space.save()
        return space
    
    @classmethod
    def find_by_space_position(cls, position):
        sql = """ SELECT * FROM spaces WHERE position = ? LIMIT 1;"""
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
            neighborhood=row[5],
            owned=[6])
    
    def __init__(self, street_name, price, rent, position, neighborhood, owned = False, id = None):
        self.street_name = street_name
        self.price = price
        self.rent = rent
        self.position = position
        self.neighborhood = neighborhood
        self.owned = owned
        self.id = id
        
    def save(self):
        sql = """INSERT INTO spaces (street_name, price, rent, position, neighborhood, owned)
            VALUES (?, ?, ?, ?, ?, ?); """
        CURSOR.execute(sql, (self.street_name, self.price, self.rent, self.position, self.neighborhood, self.owned))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    def update(self):
        sql = """UPDATE spaces
        SET street_name = ?, price = ?, rent = ?, position = ?, neighborhood = ?, owned = ?
        WHERE id = ?;"""
        CURSOR.execute(sql, (self.street_name, self.price, self.rent, self.position, self.neighborhood, self.owned, self.id))
        CONN.commit()
        
    def delete(self):
        sql = """ DELETE FROM spaces WHERE id = ?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    def __repr__(self):
        return f"<{self.street_name}: Price = {self.price}: Rent = {self.rent}: Neighborhood = {self.neighborhood}: Owned = {self.owned}>"