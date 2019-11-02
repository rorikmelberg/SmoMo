import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime

import webapp.db as wadb

class TempLog:
    def __init__(self):
        self.TempLogId = 0
        self.SensorNum = ''
        self.EventDate = ''
        self.Temp = ''
        self.CookId = 0
    
    def toString(self):
        print('TemplogId: {0}, SendorNum:{1}, EventDate: {2}, Temp: {3}, CookId: {4}'.format(self.TempLogId, self.SensorNum, self.EventDate, self.Temp, self.CookId))

def getTempsForCook(cookId):
    db = wadb.get_db()

    rtn = db.execute('SELECT TempLogId, SensorNum, EventDate, Temp, CookId '
                        'FROM TempLog WHERE CookId = ? '
                        'ORDER BY EventDate DESC', (cookId,)).fetchall()
    temps = []

    for x in rtn:
        temp = TempLog()
        temp.TempLogId = x[0]
        temp.SensorNum = x[1]
        temp.EventDate = x[2]
        temp.Temp = x[3]
        temp.CookId = x[4]
        
        temps.append(temp)
    return temps

if __name__ == "__main__":
    getTempsForCook(1)