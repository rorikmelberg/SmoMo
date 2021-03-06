import os
import functools
from webapp.db import get_db
import webapp.DAL.CookDL as CookDL
import webapp.DAL.TempDL as TempDL
import webapp.DAL.HWTempDL as HWTempDL
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

def GenerateTargetData(start, end, value):
    series = []
    
    valPair = {}
    valPair['x'] = start.strftime(dateFormatString)
    valPair['y'] = value
    series.append(valPair)

    valPair = {}
    valPair['x'] = end.strftime(dateFormatString)
    valPair['y'] = value
    series.append(valPair)

    return series

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
                                                values=temps,
                                                currentDT=datetime.now())

    @app.route('/editcook', methods=['GET', 'POST'])
    def startcook():
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
            return redirect(url_for('index'))

        else:
            if currentCookId == 0:
                return render_template('startcook.html')
            else:
                cook = CookDL.getCook(currentCookId)
                title = cook.Title
                return render_template('endcook.html', title=title)
    
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
        cookId = request.args.get('cookId')

        currentCook = CookDL.getCook(cookId)
        
        if currentCook.CookId > 0:
            allData = {}

            endTime = datetime.now()

            if currentCook.End:
                endTime = currentCook.End
            
            allData['duration'] = currentCook.Duration
            allData['cookStart']= currentCook.Start.strftime(dateFormatString)
            allData['currentDT']=datetime.now()
            
            allData['smokerTarget'] = GenerateTargetData(currentCook.Start, endTime, currentCook.SmokerTarget)
            allData['target'] = GenerateTargetData(currentCook.Start, endTime, currentCook.Target)
            currentDate = endTime
            allData['lastUpdate'] = currentDate.strftime(dateFormatString)
            
            temps = []
            
            if date:
                temps = TempDL.getTempsForCook(currentCook.CookId, date)
            else:
                temps = TempDL.getTempsForCook(currentCook.CookId)
            
            temps1 = []
            temps2 = []
            temps3 = []
            
            # get current temps from the first item in the list
            if len(temps) > 0:
                currentTemp = temps[-1]  # last in the list
                allData['Sensor1Current'] = '{0:.2f}'.format(currentTemp.Temp1)
                allData['Sensor2Current'] = '{0:.2f}'.format(currentTemp.Temp2)
                allData['Sensor3Current'] = '{0:.2f}'.format(currentTemp.Temp3)

            for x in temps:
                formattedDate = x.EventDate.strftime(dateFormatString)
                if x.Temp1 > 0:
                    temp1 = {}
                    temp1['x'] = formattedDate
                    temp1['y'] = x.Temp1
                    temps1.append(temp1)

                if x.Temp2 > 0:
                    temp2 = {}
                    temp2['x'] = formattedDate
                    temp2['y'] = x.Temp2
                    temps2.append(temp2)
                if x.Temp3 > 0:
                    temp3 = {}
                    temp3['x'] = formattedDate
                    temp3['y'] = x.Temp3
                    temps3.append(temp3)
            
            allData['Temp1'] = temps1
            allData['Temp2'] = temps2
            allData['Temp3'] = temps3

            return jsonify(allData)

        return jsonify('')


    @app.route('/recorddata', methods=['GET']) 
    def RecordData():
        cookId = CookDL.getCurrentCookId()
        
        # if DEBUG:
        #     print("CookId: {0}".format(cookId))

        if cookId > 0:
            
            # Number of samplet to take
            numOfSamples = 3

            tempSamples = []
            tempFinal = []

            for i in range(numOfSamples):
                tempSamples.append(HWTempDL.getTemps())
                tempFinal.append(0.0)

            for tempSample in tempSamples:
                tempSampleCount = 0
                for temp in tempSample:
                    tempFinal[tempSampleCount] = tempFinal[tempSampleCount] + temp
                    tempSampleCount = tempSampleCount + 1

            tempSampleCount = 0
            for temp in tempFinal:
                tempFinal[tempSampleCount] = tempFinal[tempSampleCount] / numOfSamples
                tempSampleCount = tempSampleCount + 1

            TempDL.logTemps(tempFinal, cookId)
        
        return jsonify('OK')

    from . import db
    db.init_app(app)

    return app