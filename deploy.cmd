xcopy /S /Y webapp\*.* \\tempberrypi.local\WebApp\Projects\SmokerMonitor\webapp\ /EXCLUDE:DeployExcludeList.txt
xcopy logger.py  \\tempberrypi.local\WebApp\Projects\SmokerMonitor\logger.py /Y
