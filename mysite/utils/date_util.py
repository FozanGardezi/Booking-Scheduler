from dateutil.parser import parse
from datetime import timedelta
import pytz

def getDateAccordingToHour(date, hour):
	updated_date =  updateHourInDateTime(date, hour)
	updated_date = changeDateTimeToUTC(updated_date)
	return updated_date

def formatDateAccordingToHour(date, hour):
	updated_date =  updateHourInDateTime(date, hour)
	updated_date = changeDateTimeToUTC(updated_date)
	updated_date = updated_date.strftime('%Y-%m-%d %H:%M:%S')
	return updated_date

def changeDateTimeToUTC(datetime_string):
	datetime_object = parse(datetime_string)
	return datetime_object.astimezone(pytz.UTC)

def updateHourInDateTime(datetime_string, hour):
	udpated_hour = convertHourToTwentyFourHour(hour)
	date, time = datetime_string.split("T",1)
	time = str(udpated_hour)+time[2:]
	return date+"T"+time

def convertHourToTwentyFourHour(hour):
	updated_hour = int(''.join([n for n in hour if n.isdigit()]))
	AMorPM = (''.join([n for n in hour if n.isalpha()])).upper()

	if AMorPM == "AM" and updated_hour== 12:
		new_hour_value = 00
	elif AMorPM == "AM":
		new_hour_value = updated_hour
	elif AMorPM == "PM" and updated_hour == 12: 
		new_hour_value = 12
	elif AMorPM == "PM":
		new_hour_value = 12 + updated_hour
    
	return new_hour_value

def addDays(date, days):
	return date + timedelta(days=days)

def formatDate(date, date_format):
	return date.strftime(date_format)

def subtractMinutes(date, minutes):
	return date - timedelta(minutes=minutes)