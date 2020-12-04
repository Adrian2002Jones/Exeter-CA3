'''
This is where some of the functions used in the main python document
can be tested.
'''
from datetime import date
from datetime import datetime

def tests() -> None:
    '''
    tests will be conducted here to ensure that the
    code is working as intended. Assert functions
    will be used - if an AssertionError is raised
    then we know that there has been a failure at
    some point in the program.
    '''
    #The section below is specifically for testing the function "seconds_difference"
    def seconds_difference()-> int:
        '''
        We can test this function by inserting a pre-determined
        number of hours, minutes and days into the function and
        seeing whether or not it outputs the expected result
        '''
        if remaining_minutes is not None:
            total_seconds = ((int(remaining_days) * 86400) + (int(remaining_hours) * 3600) +
                             (int(remaining_minutes) * 60))
            return total_seconds

    remaining_days = 10
    remaining_hours = 0
    remaining_minutes = 0

    def test_seconds_difference():
        '''
        if the function works correctly, then we should
        expect an input of 10 days, 0 hours and 0 minutes
        to output a value of 864000. If the answer isn't
        864000 then we get the output 'that is incorrect'
        appearing as an AssertionError
        '''
        assert seconds_difference() == 864000, 'the second_difference is incorrect'
    test_seconds_difference()

    #The section below is specifically for testing the function "minute_count_down"
    def minute_count_down()-> int:
        '''
        We can test this function by providing the 'hour_alarm'
        and 'minute_alarm' and seeing whether or not we get the
        expected output. For the purposes of this test we will
        assume that the time the function was called is 9:00
        and the time it's finding the difference to is 10:00
        '''
        total_alarm_minutes = (int(hour_alarm) * 60) + int(minute_alarm)
        current_minutes = (int(9)*60) + int(0)
        minute_difference = total_alarm_minutes - current_minutes
        return minute_difference

    hour_alarm = 10
    minute_alarm = 0

    def test_minute_count_down():
        '''
        Since we're assuming that the function is finding the
        difference in minutes between 9:00 and 10:00, we would
        expect here to see that the minute_count_down outputs 60
        '''
        assert minute_count_down() == 60, 'the test_minute_counter_down is incorrect'
    test_minute_count_down()

    #This section below is specifically for testting the function "days_between"
    def days_between(day_one: int, day_two: int) -> int:
        '''
        Since 'days_between's main purpose is to be included
        in the other function 'day_count_down' we will be
        testing both functions together since this is how
        it works in the main python document.
        '''
        day_one = datetime.strptime(day_one, "%Y-%m-%d")
        day_two = datetime.strptime(day_two, "%Y-%m-%d")
        return abs((day_one - day_two).days)

    def day_count_down()-> int:
        '''
        We can test this function by providing the variables
        and observing whether we get the number of days we
        would presume to have between the two provided dates.
        For this we will assume that the alarm is set to
        1st January 2021, and that the date we're setting the
        alarm is 1st January 2020.
        '''
        year_alarm = "21"
        month_alarm = "1"
        day_alarm = "1"
        ymd_alarm = (str(20)+year_alarm+"-"+month_alarm+"-"+day_alarm)
        day_count = days_between(str("2020-1-1"), str(ymd_alarm))
        return day_count

    def test_day_count_down():
        '''
        Between the two dates we'd expect to see 366
        days (since it's a leap year). If the function works
        than we should get the expected output below
        '''
        assert day_count_down()==366, "the minute_count_down function is incorrect"

    test_day_count_down()

    #This section below is specifically for testing the function "hour_count_down"
    def hour_count_down()-> int:
        '''
        We can test this function in a similar way to how we've
        tested the functions above: by feeding the function
        predetermined values which we already know the outcome of.
        For the purpose of this test we will be assuming that the
        alarm is set for 11:00 and is set at the 9:00. If we were
        to use the time gathered from the computer we'd never be
        able to have a consistent answer.
        '''
        alarm_date = "04/12/2020 11:00"
        if alarm_date is not None:
            hour_alarm = (alarm_date[11:13])
            current_hour = 9
            hour_difference = int(hour_alarm) - int(current_hour)
            return hour_difference

    def test_hour_count_down():
        '''
        Here, with the current predetermined values, we would
        expect the output to be 2 hours
        '''
        assert hour_count_down()==2, "the hour_count_down function is incorrect"

    test_hour_count_down()
tests()
