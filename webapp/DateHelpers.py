import datetime
import pytz

def convertTime(fromTime):
    pacific = pytz.timezone('US/Pacific')
    toTime = fromTime.astimezone(pacific)

    toTime = toTime.replace(tzinfo=None)
    return toTime
