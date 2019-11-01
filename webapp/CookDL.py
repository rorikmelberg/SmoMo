import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime

import webapp.db as wadb

class Cook:
    def __init__(self):
        self.CookId = 0
        self.Title = ''
        self.Start = ''
        self.End = ''

def getCurrentCook():
    db = wadb.get_db()

    rtn = db.execute('SELECT CookId, Title, CookStart, CookEnd FROM Cooks WHERE CookEnd is null').fetchone()
    newCook = Cook()
    
    if rtn is not None:
        newCook.CookId = rtn[0]
        newCook.Title = rtn[1]
        newCook.Start = datetime.datetime.now(rtn[2])
        newCook.End = rtn[3]
    
    return newCook

def startCook(title):
    db = wadb.get_db()
    
    db.execute('INSERT INTO Cooks (Title) VALUES(?)', (title,))
    db.commit()

def endCurrentCook():
    cook = getCurrentCook()
    db = wadb.get_db()
    db.execute('UPDATE Cooks SET CookEnd = datetime(\'now\') where CookEnd is NULL')
    db.commit()

if __name__ == "__main__":
    startCook('TestTitle')
    newCook = getCurrentCook()
    print(newCook)