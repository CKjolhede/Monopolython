# lib/helper.py
import os
import sqlite3
import random 



# Larger example that inserts many records at a time
#purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#            ]
#cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

#  exec(string)   will execute the string as regular code, string must be properly formatted
# from random import choice, sample, choices
#           names = list[str] = ['a', 'b', 'c', 'd']
            #winner: str = choice(names)
            #print(winner)     produces random selecton from list

            #winners: list[str] = sample(names, k=(#number of selections from list you want)  <-- output unique list
            #winners: list[str] = choices(names, k=(#number of selections from list you want) <-- may have repeat selections

class Helper():
    
    def blank():
        pass