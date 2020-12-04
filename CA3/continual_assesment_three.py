'''
This is the main program for CA3. This is where notifications and alarms are dealt with.
This is also where the HTML template is rendered.
'''
import sched
import logging
import time
from datetime import datetime
from datetime import date
from flask import render_template
from flask import Flask
from flask import request
import pyttsx3
from weathernewsandcovid import weatherfinder
from weathernewsandcovid import newsfinder
from weathernewsandcovid import covid_data

s = sched.scheduler(time.time, time.sleep)
schedules = []
app = Flask(__name__)
engine = pyttsx3.init()
excluded_notifications = []
excluded_alarms = []
already_added = []
alarms = []
scheduler = []
now = datetime.now()
s.run(blocking = False)
logging.info('Variables (mainly lits) are declared')

@app.route('/')
@app.route("/index")
def controller():
    '''
    This function is needed and used for the execution of everything.
    '''
    s.run(blocking = False)
    todays_weather = weatherfinder()
    todays_news = newsfinder()
    covid_num = covid_data()
    notifications = []

    def notification_add(input_notification: str) -> list[str]:
        '''
        this function acts as a shortcut to just typing
        notification.append(<whatever>). This isn't essential.
        '''
        notifications.append(input_notification)
        logging.info('A notification has been appended to the list')
        logging.info('The notification should appear on screen')

    def covid_addition() -> list[str]:
        '''
        covid_addition is responsible for appending the covid statistics to the notification array,
        meaning that this function is required for adding the covid figures to the webpage
        '''
        covid_not = {'title':'Daily Covid Cases Update' ,
                     'content': 'The latests figures state that today ('
                     +covid_num[0]+') there have been '+str(covid_num[1])+
                     ' new coronavirus cases in your local area. '
                     +str(covid_num[4])+' when compared with yesterday ('+str(covid_num[2])+')'}
        provide_covid = True
        for i in range (0, len(excluded_notifications)):
            if (excluded_notifications[i]) == ('Daily Covid Cases Update'):
                provide_covid = False
                logging.info('The covid stats have been excluded previously')
        if provide_covid:
            notification_add(covid_not)
            logging.info('The covid stats have not been excluded previously')

    def weather_addition()-> list[str]:
        '''
        weather_addition is responsible for appending the news to the notification array,
        meaning that this function is required for adding the weather to the webpage
        '''
        weather_not = {'title':'Weather Update','content': "Currently in "+todays_weather[1]+
                        " the outside temperature is "+todays_weather[2]+" along with "+
                       todays_weather[3]+" with a humidity of "+todays_weather[4]}
        provide_weather = True
        for i in range (0, len(excluded_notifications)):
            if (excluded_notifications[i]) == ('Weather Update'):
                provide_weather = False
                logging.info('The weather has been excluded previously')
        if provide_weather:
            notification_add(weather_not)
            logging.info('The weather has not been excluded previously')

    def news_addition()-> list[str]:
        '''
        news_addition is responsible for appending the news to the notification array,
        meaning that this function is required for adding the news stories to the webpage
        '''
        for i in range (0, len(todays_news)):
            provide_news = True
            news_not = {'title': todays_news[i][0],
                        'content':  todays_news[i][1]+("\n")+" Read the rest of the article here: "
                       + todays_news[i][2]}
            for j in range (0, len(excluded_notifications)):
                if todays_news[i][0] == excluded_notifications[j]:
                    provide_news = False
                    logging.info('This news article has been excluded previously')
            if provide_news:
                notification_add(news_not)
                logging.info('This news article has not been excluded previously')

    s.run(blocking = False)
    alarm_title = request.args.get("two")
    alarm_date = request.args.get("alarm")
    today = date.today()

    def days_between(day_one: int, day_two: int) -> int:
        '''
        Calculates the day difference between two
        seperate dates whilst keeping in mind the
        potential difference in months and years.
        '''
        day_one = datetime.strptime(day_one, "%Y-%m-%d")
        day_two = datetime.strptime(day_two, "%Y-%m-%d")
        return abs((day_one - day_two).days)

    def day_count_down()-> int:
        '''
        Calculates the days between
        two different dates
        '''
        if alarm_date is not None:
            year_alarm = (alarm_date[2:4])
            month_alarm = (alarm_date[5:7])
            day_alarm = (alarm_date[8:10])
            ymd_alarm = (str(20)+year_alarm+"-"+month_alarm+"-"+day_alarm)
            day_count = days_between(str(today), str(ymd_alarm))
            logging.info("User input has been provided and is being processed")
            return day_count
        else:
            logging.warning('Nothing has been input')

    def hour_count_down()-> int:
        '''
        Calculates the hour difference
        between two dates
        '''
        if alarm_date is not None:
            hour_alarm = (alarm_date[11:13])
            current_hour = int(now.strftime('%H'))
            hour_difference = int(hour_alarm) - int(current_hour)
            logging.info("The time in hours has been returned")
            return hour_difference
        else:
            logging.warning('Nothing has been input')

    def minute_count_down()-> int:
        '''
        Calculates the minute difference
        between two dates
        '''
        if alarm_date is not None:
            hour_alarm = (alarm_date[11:13])
            minute_alarm = (alarm_date[14:16])
            total_alarm_minutes = (int(hour_alarm) * 60) + int(minute_alarm)
            current_minutes = (int(now.strftime('%H'))*60) + int(now.strftime('%M'))
            minute_difference = total_alarm_minutes - current_minutes
            logging.info("The time in minutes has been returned")
            return minute_difference
        else:
            logging.warning('There has been an error creating the time')

    def seconds_difference()-> int:
        '''
        Calculates the seconds difference
        between two dates
        '''
        if remaining_minutes is not None:
            total_seconds = ((int(remaining_days) * 86400) + (int(remaining_hours) * 3600) +
                             (int(remaining_minutes) * 60))
            logging.info("The time in seconds has been returned")
            return total_seconds
        else:
            logging.warning('There has been an error creating the time')

    remaining_days = day_count_down()
    remaining_hours = hour_count_down()
    remaining_minutes = minute_count_down()
    remaining_seconds = seconds_difference()
    weather_checkbox = request.args.get("weather")
    news_checkbox = request.args.get("news")
    logging.info('Times have been declared using functions')

    excluded_notifications.append(request.args.get("alarm['title']"))

    def insert_alarm()-> list[str]:
        '''
        This function is responsible for
        the insertion of alarms onto the screen
        as well as the scheduling of these alarms
        '''
        s.run(blocking = False)
        if alarm_date is not None:
            provide_alarm = True
            for i in range (0, len(excluded_alarms)):
                if alarm_title == (excluded_alarms[i]):
                    provide_alarm = False
                    logging.info("The alarm has been excluded")
            if provide_alarm is True:
                alarm_insert = {'content': 'Alarm set for  '+str(alarm_date[8:10])+'-'+
                                str(alarm_date[5:7])+'-'+str(alarm_date[2:4])+' at '
                                +str(alarm_date[11:13])
                                + ':'+str(alarm_date[14:16])+'. Don\'t forget!',
                                'title': alarm_title}
                s.enter(remaining_seconds, 1, times_up,)
                alarms.append(alarm_insert)
                alarm_information= [remaining_seconds, alarm_title, weather_checkbox,
                                    news_checkbox]
                scheduler.append(alarm_information)
                logging.info("The alarm has been scheduled and displayed")

    def times_up():
        '''
        This function is responsible for playing the audio
        notification when a schedule is completed. What plays
        is dependent on what the user has ticked.
        '''
        if weather_checkbox is not None and news_checkbox is None:
            announcment=('This is the alarm'+alarm_title+
                        'Outside it is '+todays_weather[2]+' along with '+
                        todays_weather[3]+' with a humidity of '+todays_weather[4])
            logging.info('The announcment has been declared for the tts')

        if news_checkbox is not None and weather_checkbox is None:
            announcment=('This is the alarm'+alarm_title+
                        'Currently the latests figures state that today ('
                        +covid_num[0]+') there have been '+str(covid_num[1])+
                        ' new covid cases in your local area.')
            logging.info('The announcment has been declared for the tts')

        if weather_checkbox is not None and news_checkbox is not None:
            announcment=('This is the alarm'+alarm_title+
                         'Currently the latests figures state that today ('
                         +covid_num[0]+') there have been '+str(covid_num[1])+
                         ' new covid cases in your local area. Outside it is '+todays_weather[2]
                         +' along with '+todays_weather[3]
                         +' with a humidity of '+todays_weather[4])
            logging.info('The announcment has been declared for the tts')
        try:
            engine.endLoop()
        except:
            pass
        engine.say(announcment)
        engine.runAndWait()
        logging.info("The alarm and it's breifings has been announced")

    def remove_alarm():
        '''
        This function is responsible from removing
        the alarm from the list of alarms when the
        user clicks the "x" button on the top right
        of the tab
        '''
        remove_alarm = request.args.get("alarm_item")
        for i in range(0, len(alarms)):
            if alarms[i]['title'] == str(remove_alarm):
                alarms.pop(i)
        logging.info("The alarm tab has been removed due to the user")

    excluded_notifications.append(request.args.get("notif"))
    weather_addition()
    news_addition()
    covid_addition()
    day_count_down()
    hour_count_down()
    insert_alarm()
    remove_alarm()
    logging.info('Functions are called upon, creating the functionality')

    return render_template("ecm1400.html", title="Daily update",
                           image="covidmage.png", alarms=alarms,
                           notifications=notifications,)

if __name__ == "__main__":
    app.run()
    engine = pyttsx3.init()
    s.run(blocking = False)
