# Exeter-CA3
There's a few things which need to be done in order to make this program work as intended.

Firstly, you need to fill in the document "config.json" with the weather API (http://api.openweathermap.org/data/2.5/weather?), the news API(https://newsapi.org/v2/top-headlines?) and the location you want to know the weather and covid statistics for. For the location you need to enter the name of a city/town - entering the name of a country or a region (eg: "West Midlands") won't work. As a default this has been set to Exeter.

The imported modules used in this project are:
- sched
- logging
- time
- pyttsx3
- flask
- datetime
- requests

You will need all of these before you can run the code.


Any testable functions are displayed and tested in the test.py document.
