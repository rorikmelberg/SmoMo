#!/usr/bin/env python
import time
import re
import datetime
import os
import math
import sqlite3
import ConfigParser
import smtplib
from email.mime.text import MIMEText

def sendmail(fromaddr, toaddr, username, password, email_body, email_subject, smtpsrv, smtpport):
	# Build the email
	msg = MIMEText(email_body)
	msg['Subject'] = email_subject
	msg['From'] = fromaddr
	msg['To'] = toaddr

	try:
		# The actual mail send
		server = smtplib.SMTP(smtpsrv, smtpport)
		server.ehlo()
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddr, msg.as_string())  
		server.quit()
		#print "email sent: %s" % fromaddr

	except Exception as e:
		print('Something went wrong when sending the email {}'.format(fromaddr))
		print e



#send email if there is a msg to send
if msg != '':
	Config = ConfigParser.ConfigParser()
	Config.read("/home/pi/email.cfg")
	msgSubject = 'BBQ Monitor Alert'
	sendmail(ConfigSectionMap("Config")['smtpemail'], Email, ConfigSectionMap("Config")['smtpuser'], ConfigSectionMap("Config")['smtppass'], 
		msg, msgSubject,smtpsrv= ConfigSectionMap("Config")['smtpsrv'], smtpport= ConfigSectionMap("Config")['smtpport'])
