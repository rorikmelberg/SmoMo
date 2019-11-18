import datetime
import pytz

def convertTime(fromTime):
    pacific = pytz.timezone('US/Pacific')
    toTime = fromTime.astimezone(pacific)

    toTime = toTime.replace(tzinfo=None)
    return toTime

def printNiceTimeDelta(convert):
    if (convert.days > 0):
        out = str(convert).replace(" days, ", ":")
    else:
        out = str(convert)
        
    outAr = out.split(':')
    outAr = ["%02d" % (int(float(x))) for x in outAr]
    out   = ":".join(outAr)
    return out