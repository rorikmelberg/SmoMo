import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime

import webapp.db as wadb
import webapp.DateHelpers as dh

class Subscription:
    def __init__(self):
        self.SubscriptionId = 0
        self.CookId = ''
        self.Email = ''
    
    def toString(self):
        print('SubscriptionId: {0}, CookId: {1}, Email: {2}'.format(self.TempLogId, self.EventDate, self.Temp1, self.Temp2, self.Temp3, self.CookId))

def getSubscriptionsForCook(cookId):
    db = wadb.get_db()

    rtn = db.execute('SELECT SubscriptionId, CookId, Email '
                        'FROM Subscriptions WHERE CookId = ? ', (cookId,)).fetchall()

    subs = []

    for x in rtn:
        sub = Subscription()
        sub.SubscriptionId = x[0]
        sub.CookId = x[1]
        sub.Email = x[2]
        
        subs.append(sub)
    
    return subs

def insertSubscription(cookId, email):
    db = wadb.get_db()
    
    db.execute('INSERT INTO Subscriptions (CookId, Email) VALUES(?,?)', (cookId, email,))
    
    db.commit()

def delete(subscriptionId):
    db = wadb.get_db()
    db.execute('DELETE FROM Subscriptions WHERE SubscriptionId = ?', (subscriptionId,))
    db.commit()


if __name__ == "__main__":
    getSubscriptionsForCook(1)