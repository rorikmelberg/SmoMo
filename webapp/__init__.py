import os
import functools
from webapp.db import get_db
import webapp.CookDL as CookDL

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
        s1Min = ''
        s1Max = ''
        s2Min = ''
        s2Max = ''
        airMin = ''
        airMax = ''

        if currentCook.CookId > 0:
            title = currentCook.Title
            start = currentCook.Start
            print(currentCook.Start)
            print(datetime.now())
            print(type(currentCook.Start))
            print(type(datetime.now()))

            calcDuration = (currentCook.Start - datetime.now())
            print(calcDuration)
            duration = "{0} h {1} m".format(calcDuration.hour, calcDuration.minute)

        return render_template('index.html', title = title, 
                                                start = start, 
                                                duration = duration, 
                                                s1Min = s1Min,
                                                s1Max = s1Max,
                                                s2Min = s2Min,
                                                s2Max = s2Max,
                                                airMin = airMin,
                                                airMax = airMax)

    @app.route('/startcook', methods=['GET', 'POST'])
    def startcook():
        if request.method == "POST":
            title = request.form["title"]
            CookDL.startCook(title)
            return redirect('\\')
        else:
            currentCook = CookDL.getCurrentCook()
            if currentCook.CookId > 0:
                return render_template('endcook.html', title=title)    
            
            return render_template('startcook.html')

    @app.route('/endcook', methods=['GET', 'POST'])
    def endcook():
        if request.method == "POST":
            CookDL.endCurrentCook()
            return redirect('\\')
        else:
            currentCook = CookDL.getCurrentCook()
            if currentCook.CookId == 0:
                return render_template('startcook.html')    
            
            title = currentCook.Title
            return render_template('endcook.html', title=title)



    from . import db
    db.init_app(app)

    from . import cook
    app.register_blueprint(cook.bp)

    return app