import os
import functools
from webapp.db import get_db
import webapp.DAL.CookDL as CookDL
import webapp.DAL.TempDL as TempDL
# only import if running on the PI
import webapp.DAL.HWTempDL as HWTempDL

import webapp.BO.CookBO as CookBO

from datetime import datetime

from flask import jsonify

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

def GetCookData(cookId, date):
    
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
    
    return jsonify('')

# def ProcessSubscriptions(CookId)
