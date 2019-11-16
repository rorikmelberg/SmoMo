import os
import functools
from webapp.db import get_db
import webapp.CookDL as CookDL
import webapp.TempDL as TempDL

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import  url_for
from flask import Flask, render_template
from flask import jsonify

from datetime import datetime

def GenerateTargetData(start, end, value):
    series = []
    
    valPair = {}
    valPair['x'] = start.strftime('%Y-%m-%d %H:%M:%S.%s')
    valPair['y'] = value
    series.append(valPair)

    valPair = {}
    valPair['x'] = end.strftime('%Y-%m-%d %H:%M:%S.%s')
    valPair['y'] = value
    series.append(valPair)

    return series

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    @app.route('/index')
    def index():
        currentCook = CookDL.getCurrentCook()
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
                                                values=temps,
                                                currentDT=datetime.now())

    @app.route('/editcook', methods=['GET', 'POST'])
    def startcook():
        currentCook = CookDL.getCurrentCook()
        if request.method == "POST":
            if currentCook.CookId == 0:
                title = request.form["title"]
                smokerTarget =  request.form["smokerTarget"]
                target =  request.form["target"]
                CookDL.startCook(title, smokerTarget, target)
            else:
                CookDL.endCurrentCook()    
            return redirect(url_for('index'))

        else:
            if currentCook.CookId == 0:
                return render_template('startcook.html')
            else:
                title = currentCook.Title
                return render_template('endcook.html', title=title)


    @app.route('/getdata', methods=['GET']) 
    def add_numbers():
        currentCook = CookDL.getCurrentCook()
        if currentCook.CookId > 0:
            allData = {}
            
            date = request.args.get('lastUpdate')

            allData['duration'] = currentCook.Duration
            # allData['latestTime'] = ,
            # allData['latestTemp'] = latestTemp,
            allData['cookStart']= currentCook.Start.strftime('%Y-%m-%d %H:%M:%S.%s')
            allData['currentDT']=datetime.now()
            
            allData['smokerTarget'] = GenerateTargetData(currentCook.Start, datetime.now(), currentCook.SmokerTarget)
            allData['target'] = GenerateTargetData(currentCook.Start, datetime.now(), currentCook.Target)
            currentDate = datetime.now()
            allData['lastUpdate'] = currentDate.strftime('%Y-%m-%d %H:%M:%S.%s')
            
            temps = []
            
            if date:
                temps = TempDL.getTempsForCookUpdate(currentCook.CookId, date)
            else:
                temps = TempDL.getTempsForCook(currentCook.CookId)
            
            temps1 = []
            temps2 = []
            temps3 = []
            
            if len(temps) > 0:
                allData['Sensor1Current'] = temps[0].Temp1
                allData['Sensor2Current'] = temps[0].Temp1
                allData['Sensor3Current'] = temps[0].Temp1


            for x in temps:
                formattedDate = x.EventDate.strftime('%Y-%m-%d %H:%M:%S.%s')

                temp1 = {}
                temp1['x'] = formattedDate
                temp1['y'] = x.Temp1
                temps1.append(temp1)

                temp2 = {}
                temp2['x'] = formattedDate
                temp2['y'] = x.Temp2
                temps2.append(temp2)

                temp3 = {}
                temp3['x'] = formattedDate
                temp3['y'] = x.Temp3
                temps3.append(temp3)
            
            allData['Temp1'] = temps1
            allData['Temp2'] = temps2
            allData['Temp3'] = temps3

            return jsonify(allData)

        return jsonify('')

    from . import db
    db.init_app(app)

    from . import cook
    app.register_blueprint(cook.bp)

    return app