import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime

import webapp.db as wadb
import webapp.DateHelpers as dh

class TempLog:
    def __init__(self):
        self.TempLogId = 0
        self.EventDate = ''
        self.Temp1 = ''
        self.Temp2 = ''
        self.Temp3 = ''
        self.CookId = 0
    
    def toString(self):
        print('TemplogId: {0}, EventDate: {1}, Temp1: {2}, Temp2: {3}, Temp3: {4}, CookId: {5}'.format(self.TempLogId, self.EventDate, self.Temp1, self.Temp2, self.Temp3, self.CookId))

def getTempsForCook(cookId):
    db = wadb.get_db()

    rtn = db.execute('SELECT TempLogId, EventDate, Temp1, Temp2, Temp3, CookId '
                        'FROM TempLog WHERE CookId = ? '
                        'ORDER BY EventDate DESC', (cookId,)).fetchall()
    temps = []

    for x in rtn:
        temp = TempLog()
        temp.TempLogId = x[0]
        temp.EventDate = dh.convertTime(x[1])
        temp.Temp1 = x[2]
        temp.Temp2= x[3]
        temp.Temp3 = x[4]
        temp.CookId = x[5]
        
        temps.append(temp)
    return temps

if __name__ == "__main__":
    getTempsForCook(1)