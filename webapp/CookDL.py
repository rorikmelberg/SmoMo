import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import webapp.DateHelpers as dh
import webapp.db as wadb

from datetime import datetime

class Cook:
    def __init__(self):
        self.CookId = 0
        self.Title = ''
        self.Start = ''
        self.End = ''
        self.SmokerTarget = 0
        self.Target = 0
        self.Duration = ''

def getCurrentCook():
    db = wadb.get_db()

    rtn = db.execute('SELECT CookId, Title, CookStart, CookEnd, SmokerTarget, Target FROM Cooks WHERE CookEnd is null').fetchone()
    newCook = Cook()
    
    if rtn is not None:
        newCook.CookId = rtn[0]
        newCook.Title = rtn[1]
        newCook.Start = rtn[2]
        newCook.End = rtn[3]
        newCook.SmokerTarget = rtn[4]
        newCook.Target = rtn[5]

        calcDuration = (datetime.now() - newCook.Start)
        newCook.Duration = str(calcDuration)
    return newCook

def startCook(title, smokerTarget, target):
    db = wadb.get_db()
    
    db.execute('INSERT INTO Cooks (Title, CookStart, SmokerTarget, Target) VALUES(?,?,?,?)', (title, datetime.now(), smokerTarget, target,))
    db.commit()

def endCurrentCook():
    db = wadb.get_db()
    db.execute('UPDATE Cooks SET CookEnd = datetime(\'now\') where CookEnd is NULL')
    db.commit()

if __name__ == "__main__":
    startCook('TestTitle')
    newCook = getCurrentCook()
    print(newCook)