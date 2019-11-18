from flask import session

def setCookId(cookId):
    session['CookId'] = cookId

def getCookId():
    cookId = session.get('CookId', 0)
    return cookId