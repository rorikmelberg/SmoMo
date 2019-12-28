import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import webapp.DateHelpers as dh
import webapp.db as wadb

from datetime import datetime

dateFormatter = '%m/%d/%Y - %H:%M:%S'

class Cook:
    def __init__(self):
        self.CookId = 0
        self.Title = ''
        self.Start = ''
        self.End = ''
        self.StartFormatted = ''
        self.EndFormatted = ''
        self.SmokerTarget = 0
        self.Target = 0
        self.Duration = ''

def getCurrentCookId():
    db = wadb.get_db()

    rtn = db.execute('SELECT CookId FROM Cooks WHERE CookEnd is null').fetchone()
    
    if rtn is not None:
        return rtn[0]
    else:
        return 0

def getCook(cookId):
    db = wadb.get_db()
    
    rtn = db.execute('SELECT CookId, Title, CookStart, CookEnd, SmokerTarget, Target FROM Cooks WHERE CookId = ?', (str(cookId), )).fetchone()
    if rtn:
        cook = objectifyCook(rtn)
    else:
        cook = Cook()
    return cook

def getCooks():
    db = wadb.get_db()

    rtn = db.execute('SELECT CookId, Title, CookStart, CookEnd, SmokerTarget, Target FROM Cooks').fetchall()
    cooks = []
    
    if rtn is not None:
        for x in rtn:
            cook = objectifyCook(x)
            cooks.append(cook)
    return cooks

def delete(cookId):
    db = wadb.get_db()

    rtn = db.execute('DELETE FROM TempLog where CookId = ?', (cookId,))
    rtn = db.execute('DELETE FROM Cooks where CookId = ?', (cookId,))

    db.commit()

def objectifyCook(cookList):
    cook = Cook()
    
    cook.CookId = cookList[0]
    cook.Title = cookList[1]
    cook.Start = cookList[2]
    cook.End = cookList[3]
    cook.SmokerTarget = cookList[4]
    cook.Target = cookList[5]
    cook.StartFormatted = cook.Start.strftime(dateFormatter)
    
    if cook.End:
        fromTime = cook.End
        cook.EndFormatted = cook.End.strftime(dateFormatter)
    else:
        fromTime = datetime.now()
        cook.EndFormatted = 'Running'

    calcDuration = (fromTime - cook.Start)
    cook.Duration = dh.printNiceTimeDelta(calcDuration)
    return cook

def startCook(title, smokerTarget, target):
    db = wadb.get_db()
    
    db.execute('INSERT INTO Cooks (Title, CookStart, SmokerTarget, Target) VALUES(?,?,?,?)', (title, datetime.now(), smokerTarget, target,))
    db.commit()

def endCurrentCook():
    db = wadb.get_db()
    db.execute('UPDATE Cooks SET CookEnd = ? where CookEnd is NULL', (datetime.now(),))
    db.commit()

if __name__ == "__main__":
    startCook('TestTitle', 123, 123)
    newCook = getCurrentCookId()
    print(newCook)