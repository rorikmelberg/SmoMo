import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math

def main():
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.CE0)
    
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    
    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
    
    while True:
        print('Raw ADC Value: ', chan.value)
        print('ADC Voltage: ' + str(chan.voltage) + 'V')
        print('Temp: {0}'.format(temp_calc(chan.voltage)))
        time.sleep(2)

def temp_calc(value):
    volts = value #  (value * 3.3) / 1024 #calculate the voltage
    ohms = ((1/volts)*3300)-1000 #calculate the ohms of the thermististor

    lnohm = math.log1p(ohms) #take ln(ohms)

    #a, b, & c values from http://www.thermistor.com/calculators.php
    #using curve R (-6.2%/C @ 25C) Mil Ratio X
    #a =  0.002197222470870
    #b =  0.000161097632222
    #c =  0.000000125008328

    a =  0.000570569668444 
    b =  0.000239344111326 
    c =  0.000000047282773 

    #Steinhart Hart Equation
    # T = 1/(a + b[ln(ohm)] + c[ln(ohm)]^3)

    t1 = (b*lnohm) # b[ln(ohm)]

    c2 = c*lnohm # c[ln(ohm)]

    t2 = math.pow(c2,3) # c[ln(ohm)]^3

    temp = 1/(a + t1 + t2) #calcualte temperature

    tempc = temp - 273.15 - 4 #K to C

    tempf = tempc*9/5 + 32
    # the -4 is error correction for bad python math

    #print out info
    print ("%4d/1023 => %5.3f V => %4.1f ohms  => %4.1f K => %4.1f C  => %4.1f F" % (value, volts, ohms, temp, tempc, tempf))

    return tempf

if __name__ == "__main__":
    main()