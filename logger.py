import time
import datetime
import os
import math
import sqlite3

import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Set debug = 1 if you want the debug output
DEBUG = 0

def main():
    
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.CE0)
    
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    
    channels = [MCP.P0, MCP.P1, MCP.P2]

    for channel in channels:

        # create an analog input channel on pin 0
        chan = AnalogIn(mcp, channel)
        value = chan.value
        
        if DEBUG:
            print('Value: {0} Voltage: {1}'.format(value, chan.voltage))
        
        if value != 0:
            temp = temp_calc(chan.voltage)
            temp = int(temp)
            if DEBUG:
                print("value: {0} {1} {2}".format(value, temp, channel))
            
            log_temperature(channel, temp)

        #log temperature of 0 if sensor is not connected
        if value == 0:
            if DEBUG:
                print("value: {0} {1}".format(value, channel))
            
            log_temperature(channel, 0)

def temp_calc(volts):
    ohms = ((1/volts)*3300)-1000 #calculate the ohms of the thermististor

    lnohm = math.log1p(ohms) #take ln(ohms)

    # a, b, & c values from http://www.thermistor.com/calculators.php
    # using curve R (-6.2%/C @ 25C) Mil Ratio X
    a =  0.000570569668444 
    b =  0.000239344111326 
    c =  0.000000047282773 

    #Steinhart Hart Equation
    # T = 1/(a + b[ln(ohm)] + c[ln(ohm)]^3)
    t1 = (b*lnohm) # b[ln(ohm)]
    c2 = c*lnohm # c[ln(ohm)]
    t2 = math.pow(c2,3) # c[ln(ohm)]^3

    temp = 1/(a + t1 + t2) #calcualte temperature
    tempc = temp - 273.15 #K to C  Did have a - 4, removed because?
    tempf = tempc * 9/5 + 32
    
    if DEBUG:
        #print out info
        print ("%5.3f V => %4.1f ohms  => %4.1f K => %4.1f C  => %4.1f F" % (volts, ohms, temp, tempc, tempf))

    return tempf
    
def log_temperature(sensorNum,temp):

    conn=sqlite3.connect('/home/pi/Projects/SmokerMonitor/instance/flaskr.sqlite')
    curs=conn.cursor()
    curs.execute("INSERT INTO TempLog (SensorNum,Temp) values((?), (?))", (sensorNum, temp))

    # commit the changes
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()