#!/bin/bash
# Script to load the application
cd /home/pi/Projects/SmokerMonitor/

set FLASK_APP=webapp
set FLASK_ENV=development
flask run --port 80 --host 0.0.0.0

