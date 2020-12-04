'''
Modules here can be used in the main function, weather, news and covid information
can be returned by the modules listed below
'''
import logging
from datetime import datetime
from requests import get
import requests

logging.basicConfig(level=logging.DEBUG, filename='continual_assesment_log.log', encoding='utf-8')


lines = open('config.json','r').readlines()

API_weather_key= (lines[1])
split_API_weather_key = API_weather_key.split(' ')
weather_api_key = split_API_weather_key[3]
logging.info('The weather API key should be retrieved from the config.json file')


API_news_key = (lines[2])
split_API_news_key = API_news_key.split(' ')
news_api_key = split_API_news_key[3]
logging.info('The news API key should be retrieved from the config.json file')


location = (lines[3])
split_location = location.split(' ')
user_location = split_location[2]
logging.info('The input location should be retrieved from the config.json file')


now = datetime.now()
current_time = now.strftime("%H:%M")

def weatherfinder()-> list[str]:
    '''
    Uses the users location (specified in config) and finds the weather in that location
    at that exact moment
    '''
    api_key = weather_api_key
    city_name = user_location
    complete_url = ("http://api.openweathermap.org/data/2.5/weather?" + "appid="
                    + api_key + "&q=" + city_name)
    response = requests.get(complete_url)
    weather_response = response.json()

    logging.info('All of the nessisary weather information regarding the is retrieved')

    des=(list(weather_response.items())[1][1][0])
    tem=(list(weather_response.items())[3][1])
    hum=(list(weather_response.items())[3][1])
    humid=(list(hum.values()))
    desc=(list(des.values()))
    temp=(list(tem.values()))
    kelvin_temp = temp[0]
    cel_temp = int(kelvin_temp) - 273.15
    format_cel_temp = "{:.1f}".format(cel_temp)
    weatherinfo = (current_time, city_name, format_cel_temp+"°C", desc[2], str(humid[5])+"%")
    logging.info('info regarding the weather, as well as the time and location is returned.')
    return weatherinfo

def newsfinder()-> list[str]:
    '''
    Get's the 10 most important news stories, filters for the word "covid" (or any alternative)
    and returns the remaining stories
    '''
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = news_api_key
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    complete_page = (response.json())
    logging.info('All of the news stories have been retrieved from the news api by this point')
    twenty_stories = []
    for i in range(0, 20):
        article=(list(complete_page.items())[2][1][i])
        broken_down_article = (list(article.values()))
        headline=(broken_down_article[2])
        description=(broken_down_article[3])
        url=(broken_down_article[4])
        full_story = (headline, description, url)
        cnews = full_story[0]
        if ("COVID" in cnews or "Covid" in cnews or "covid" in cnews
            or "Coronavirus" in cnews or "coronavirus" in cnews):
            twenty_stories.append(full_story)
    logging.info('The top 20 news stories have been searched and any story regarding COVID')
    return twenty_stories

def covid_data()-> list[str]:
    '''
    Gets useful data using the information the user input as well as a covid API
    '''
    endpoint = ('https://api.coronavirus.data.gov.uk/v1/data?''filters=areaName='+
                (user_location)+'&''structure={"date":"date","newCases":"newCasesByPublishDate"}')
    response = get(endpoint, timeout=10)
    data = response.json()
    logging.info('All of the covid statistics in the local area have been retrieved')
    yesterday_list=(list(data.items())[2][1][1])
    yesterday=(list(yesterday_list.items()))
    latest_yesterday = yesterday[0][1]
    latest_yesterday_cases = yesterday[1][1]
    todaylist=(list(data.items())[2][1][0])
    today=(list(todaylist.items()))
    latest_day = today[0][1]
    latest_cases = today[1][1]
    percentage_change = (latest_cases - latest_yesterday_cases)/latest_yesterday_cases * 100
    two_dp_percentage = "{:.2f}".format(percentage_change)
    if percentage_change > 0:
        percentage = "New cases have risen by "+(two_dp_percentage)+"%"
    else:
        percentage = "New cases have fallen by "+str(-1*float(two_dp_percentage))+"%"

    covid_information = (latest_day, latest_cases, latest_yesterday,
                         latest_yesterday_cases, percentage)
    logging.info('Covid statistics, including percentages and precise numbers are returned')
    return covid_information
