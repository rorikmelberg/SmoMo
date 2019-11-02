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

from datetime import datetime

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
    def index():
        currentCook = CookDL.getCurrentCook()
        title = ''
        start = ''
        duration = ''
        latestTime = [datetime(2019,1,1), datetime(2019,1,1), datetime(2019,1,1)]
        latestTemp = [0, 0, 0]
        minTemp = [9999, 9999, 9999]
        maxTemp = [0, 0, 0]
        temps = []
        
        if currentCook.CookId > 0:
            title = currentCook.Title
            start = currentCook.Start
            calcDuration = (datetime.now() - currentCook.Start)
            duration = str(calcDuration)

            temps = TempDL.getTempsForCook(currentCook.CookId)

          
            for x in temps:
                if x.EventDate > latestTime[x.SensorNum]:
                    latestTime[x.SensorNum] = x.EventDate
                    latestTemp[x.SensorNum] = x.Temp
                
                if x.Temp < minTemp[x.SensorNum]:
                    minTemp[x.SensorNum] = x.Temp
                
                if x.Temp > maxTemp[x.SensorNum]:
                    maxTemp[x.SensorNum] = x.Temp

        return render_template('index.html', title = title, 
                                                start = start, 
                                                duration = duration, 
                                                latestTime = latestTime,
                                                latestTemp = latestTemp,
                                                minTemp = minTemp,
                                                maxTemp = maxTemp,
                                                temps = temps)

    @app.route('/editcook', methods=['GET', 'POST'])
    def startcook():
        currentCook = CookDL.getCurrentCook()
        if request.method == "POST":
            if currentCook.CookId == 0:
                title = request.form["title"]
                CookDL.startCook(title)
            else:
                CookDL.endCurrentCook()    
            return redirect('\\')

        else:
            if currentCook.CookId == 0:
                return render_template('startcook.html')
            else:
                title = currentCook.Title
                return render_template('endcook.html', title=title)

    from . import db
    db.init_app(app)

    from . import cook
    app.register_blueprint(cook.bp)

    return app