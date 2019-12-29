import os
import functools
from webapp.db import get_db
import webapp.DAL.SubscriptionDL as SubscriptionDL
import webapp.DAL.CookDL as CookDL
import webapp.DAL.EmailDL as EmailDL
from datetime import datetime

from flask import jsonify

def ProcessSubscriptions(cookId, target, smokerTarget, temp1, temp2, smokerTemp):
    cook = CookDL.getCook(cookId)
    subs = SubscriptionDL.getSubscriptionsForCook(cookId)

    alertEmail = ''

    # deadband for smoker = 10%
    smokerHigh = smokerTarget * 1.1
    smokerLow = smokerTarget * 0.9
    
    if smokerTemp > smokerHigh:
        alertEmail = alertEmail + 'Smoker Temp is high. Target = {} Actual = {}'.format(smokerTarget, smokerTemp)
        
    if smokerTemp < smokerLow:
        alertEmail = alertEmail + 'Smoker Temp is low. Target = {} Actual = {}'.format(smokerTarget, smokerTemp)

    # Alert when meat has gone within 5 deg of target
    if temp1 > target - 5 || Temp2 > temp1 - 5:
        alertEmail = alertEmail + 'Target Temp within 5 degrees: Target = {} Temp1 = {} Temp2 = {}'.format(smokerTarget, temp1, temp2)

    # Alert when meat has hit target
    if temp1 >= target || temp2 >= target:
        alertEmail = alertEmail + 'Target Temp hit: Target = {} Temp1 = {} Temp2 = {}'.format(smokerTarget, temp1, temp2)

    # Alert when meat has hit + 5 deg of target
    if temp1 >= target + 5 || temp2 >= target + 5:
        alertEmail = alertEmail + 'Target Temp over by 5 degrees: Target = {} Temp1 = {} Temp2 = {}'.format(smokerTarget, temp1, temp2)

    for sub in subs:
        EmailDL.SendMessage(alertEmail)
