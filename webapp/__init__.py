import os
import functools
from webapp.db import get_db
import webapp.DAL.CookDL as CookDL
import webapp.DAL.TempDL as TempDL
import webapp.DAL.SubscriptionDL as SubscriptionDL
import webapp.BO.CookBO as CookBO
import webapp.SMSession as SMSession

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask, render_template, session
from flask import jsonify
from flask_session.__init__ import Session
from datetime import datetime

dateFormatString = '%Y-%m-%d %H:%M:%S.%f'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # app.config.from_object(__name__)
    Session(app)

    @app.route('/')
    @app.route('/index')
    def index():
        cookId = SMSession.getCookId()
        
        if cookId == 0:
            cookId = CookDL.getCurrentCookId()
            SMSession.setCookId(cookId)
        
        currentCook = CookDL.getCook(cookId)

        latestTime = datetime(2019,1,1)
        latestTemp = [0, 0, 0]
        minTemp = [9999, 9999, 9999]
        maxTemp = [0, 0, 0]
        temps = []

        if currentCook.CookId > 0:
            temps = TempDL.getTempsForCook(currentCook.CookId)

            for x in temps:
                if x.EventDate > latestTime:
                    latestTime = x.EventDate
                    latestTemp[0] = x.Temp1
                    latestTemp[1] = x.Temp2
                    latestTemp[2] = x.Temp3
                """
                if x.Temp < minTemp[x.SensorNum]:
                    minTemp[x.SensorNum] = x.Temp
                
                if x.Temp > maxTemp[x.SensorNum]:
                    maxTemp[x.SensorNum] = x.Temp
                """
                
        return render_template('index.html', cook = currentCook, 
                                                latestTime = latestTime,
                                                latestTemp = latestTemp,
                                                minTemp = minTemp,
                                                maxTemp = maxTemp,
                                                temps = temps,
                                                values = temps,
                                                currentDT=datetime.now())

    @app.route('/editcook', methods=['GET', 'POST'])
    def editcook():
        currentCookId = CookDL.getCurrentCookId()

        if request.method == "POST":
            if currentCookId == 0:
                title = request.form["title"]
                smokerTarget =  request.form["smokerTarget"]
                target =  request.form["target"]
                CookDL.startCook(title, smokerTarget, target)
                cookId = CookDL.getCurrentCookId()
                SMSession.setCookId(cookId)
            else:
                CookDL.endCurrentCook()    
            
            return redirect(url_for('editcook'))

        else:
            cook = CookDL.getCook(currentCookId)
            subs = SubscriptionDL.getSubscriptionsForCook(currentCookId)
            title = cook.Title
            return render_template('editcook.html', cook = cook,
                                                    subs = subs)
    
    @app.route('/addsubscription', methods=['POST'])
    def addsubscription():
        email = request.form["Email"]
        cookId = request.form["CookId"]
        SubscriptionDL.insertSubscription(cookId, email)
        return redirect(url_for('editcook'))

    @app.route('/deletesub', methods=['GET'])
    def deletesubscription():
        subscriptionId = request.args.get('subscriptionId')
        SubscriptionDL.delete(subscriptionId)
        return redirect(url_for('editcook'))

    @app.route('/selectcook', methods=['GET']) 
    def selectCook():
        cookId = request.args.get('cookId')

        if cookId:
            SMSession.setCookId(cookId)
            return redirect(url_for('index'))

        else:
            cooks = CookDL.getCooks()
            return render_template('selectcook.html', cooks=cooks)

    @app.route('/deletecook', methods=['GET']) 
    def deleteCook():
        
        cookId = request.args.get('cookId')
        CookDL.delete(cookId)
        return redirect(url_for('selectCook'))

    @app.route('/getdata', methods=['GET']) 
    def GetCookData():
        date = request.args.get('lastUpdate')
        forceUpdate = request.args.get('forceUpdate')
        cookId = request.args.get('cookId')

        if(forceUpdate):
            RecordData()

        return CookBO.GetCookData(cookId, date)

    @app.route('/recorddata', methods=['GET']) 
    def RecordData():
        CookBO.RecordData()
        return jsonify('')

    from . import db
    db.init_app(app)
    
    return app
