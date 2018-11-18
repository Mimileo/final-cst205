'''
    File name: practice_weather.py

    Author: Mireya Leon

    Date created: 8/5/2018

    Date last modified: 11/17/2018

    Course Name: CST 205: Multimedia Programming

    Description: initilaize flask app. The user's searched word is retrieved from the form. This is used in the weather api query parameter. 
    Retrieved data from the api is stored in variables. The forecast api creates weather objects from the interval waether reports, 
    then each object is stored a lsit of the corresponding day

    
'''

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
import time
from dateutil import tz
import tzlocal
import pytz
import re
import calendar
from tzwhere import tzwhere
from pytz import timezone
import requests
from collections import defaultdict


app = Flask(__name__)

Bootstrap(app)

class DailyWeather():
	def __init__(self, description='',pic=None, dt=None, temp=None, time='', dt_m=''):
		self.description = description
		self.pic = pic
		self.dt = dt
		self.temp=temp
		self.time=time
		self.dt_m=dt_m

	def __str__(self):
		return "Desciption: {}, Temp: {}".format(self.description, self.temp)

def getZone(lat, lon):
	tzw = tzwhere.tzwhere()
	timezone_str = tzw.tzNameAt(lat, lon) # Seville coordinates
	return timezone_str

def convert_pst(suntime, time_z):
	
	local_tz = pytz.timezone(time_z)
	utc_dt = datetime.utcfromtimestamp(suntime).replace(tzinfo=pytz.utc)
	local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))
	return local_dt.strftime("%-I:%M:%S %p")
	'''from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('America')
	rise = datetime.utcfromtimestamp(suntime).strftime('%Y-%m-%d %H:%M:%S')
	utc = datetime.strptime(rise, '%Y-%m-%d %H:%M:%S')
	utc = utc.replace(tzinfo=from_zone)
	pacific=utc.astimezone(to_zone)'''
	'''unix = float(suntime)
	local_timezone = tzlocal.get_localzone()
	local_time = datetime.fromtimestamp(unix, local_timezone)
	military = local_time.strftime("%H:%M:%S")
	return datetime.strptime(military, "%H:%M:%S").strftime("%-I:%M:%S %p")'''
def getMonth(year, month, day):
	number = int(month)
	m =''
	d = str(int(day))
	print(d)
	if number == 1:
		m = "Jan"
	elif number == 2:
		m = "Feb"
	elif number == 3:
		m = "Mar"
	elif number == 4:
		m = "Apr"
	elif number == 5:
		m = "May"
	elif number == 6:
		m = "Jun"
	elif number == 7:
		m = "Jul"
	elif number == 8:
		m =  "Aug"
	elif number == 9:
		m = "Sep"
	elif number == 10:
		m = "Oct"
	elif number == 11:
		m = "Nov"
	elif number == 12:
		m = "Dec"
	return m + ' ' + d + ', ' + year


def getDate(timestamp):
	'''print(time.ctime(timestamp))
	print(datetime.fromtimestamp(timestamp))
	local_timezone = tzlocal.get_localzone()
	print(datetime.fromtimestamp(timestamp,local_timezone))'''
	unix = float(timestamp)
	local_timezone = tzlocal.get_localzone()
	local_time = datetime.fromtimestamp(unix, local_timezone)
	return local_time.strftime("%a %b %-d, %Y")

@app.route('/temperature', methods=['POST'])
def temperature():

	city = request.form['city']
	if not city:
		error = "Error: Enter a city name"
		return render_template('index.html', error=error)
	else:
		search = [x for x in re.split(',| ',city) if x!='']
		items = len(search)
		if items == 1:
			city = search[0]
			print(city)
		elif items == 2: 
			city = search[0] + ',' + search[1]
			print(city)
		else:
			error = "Error: Enter a one country name and one country code"
			return render_template('index.html', error=error)

	api_key = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=59903fb79cf3bf6d95a4d822609b0402'

	url = api_key 

	
	
    
	item = requests.get(url).json()
	print(item)

	if item['cod'] == '404':
		error = "Error: Your City Was Not Found!"
		return render_template('index.html', error=error)
	else:
		#result = json_object
		country = item['sys']['country']
		lat = item['coord']['lat']
		lon = item['coord']['lon']
		time_z = getZone(lat,lon)
		temp_k = item['main']['temp']
		temp = round( ( (temp_k - 273.15) * 9/5 + 32), 2 )
		wind_speed = item['wind']['speed']
		sunrise = item['sys']['sunrise']
		pacific =convert_pst(sunrise, time_z)
		date = getDate(item['dt'])
		'''utc = datetime.strptime(rise, '%Y-%m-%d %H:%M:%S')
		utc = utc.replace(tzinfo=from_zone)
		pacific=utc.astimezone(to_zone)'''

		sundown = item['sys']['sunset']
		pacific_down = convert_pst(sundown, time_z)
		'''sunset = datetime.utcfromtimestamp(sundown).strftime('%Y-%m-%d %H:%M:%S')
		utc = datetime.strptime(sunset, '%Y-%m-%d %H:%M:%S')
		utc = utc.replace(tzinfo=from_zone)
		pacific_down=utc.astimezone(to_zone)'''

		description = item['weather'][0]['description']
		icon = item['weather'][0]['icon']
		#icon = "http://openweathermap.org/img/w/"+ geticon +"png"
		name = item['name']

	return render_template('temperature.html', **locals())
		
	'''temp_k = json_object['main']['temp']
	temp_f = (temp_k - 273.15) * 1.8 + 32
	temp = float(round(temp_f,2))'''
@app.route('/forecast/<id>')
def forecast(id):
	print(id)
	city = id
	
	api_key = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&appid=59903fb79cf3bf6d95a4d822609b0402'

	url = api_key 
    
	item = requests.get(url).json()
	print(item)

	if item['cod'] == '404':
		error = "Error: Your City Was Not Found!"
		return render_template('index.html', error=error)
	else:
		
		curr_dt = ''
		forecast = []
		for i in item['list']:
			
			time = i['dt_txt']

			next_dt, hour = time.split(' ')

			
			if curr_dt != next_dt:
				curr_dt = next_dt
				year, month, day = curr_dt.split('-')
				dt_mon = getMonth(year, month, day)
				dt = {'y': year, 'm': month, 'd': day}
				print('\n{m}/{d}/{y}'.format(**dt))
				
				dt_f = '\n{m}/{d}/{y}'.format(**dt)
				
			date_f = getDate(i['dt'])
			
			hour = int(hour[:2])

			if hour < 12:
				if hour == 0:
					hour = 12
				meridiem = 'AM'
			else:
				if hour > 12:
					hour -= 12
				meridiem = 'PM'

			print('\n%i:00 %s' % (hour, meridiem))

			temp = i['main']['temp']
			description = i['weather'][0]['description']

			print("Weather: " + description)
			print('Temperature %.2f' % (temp * 9/5 - 459.67))

			temp_f = round( ( (temp - 273.15) * 9/5 + 32), 2 )

			daily_weather = DailyWeather(
				pic = i['weather'][0]['icon'],
				description = i['weather'][0]['description'],
				temp = temp_f,
				dt = i['dt_txt'],
				time = '\n%i:00 %s' % (hour, meridiem),
				dt_m = dt_mon
			)
			forecast.append(daily_weather)
			

			

		cal = calendar.month(int(year), int(month))
		print('\n' + cal)

		print(len(forecast))
		
		dates=[]
		for i in forecast:
			dates.append(i.dt[0:10])
		unique_dates = list(sorted(set(dates)))
		print(unique_dates)
		days1 = []
		days2 = []
		days3 = []
		days4 = []
		days5 = []
		days6 = []

		date = unique_dates[0]
		date2 = unique_dates[1]
		date3 = unique_dates[2]
		date4 = unique_dates[3]
		date5 = unique_dates[4]

		if len(unique_dates) == 6:
			date6 = unique_dates[5]

		for i in forecast:
			find = i.dt[0:10]
			if date == find:
				days1.append(i)
				#print(i.dt)
			elif find == date2:
				days2.append(i)
			elif find == date3:
				days3.append(i)
			elif find == date4:
				days4.append(i)
			elif find == date5:
				days5.append(i)
			elif find == date6 and len(unique_dates) == 6:
				days6.append(i)
			else:
				print("No more vals")
				break
		
		for i in days1:
			print(i)
			print(i.dt)
		for i in days2:
			print(i)
			print(i.dt)
		for i in days3:
			print(i)
			print(i.dt)
		for i in days4:
			print(i)
			print(i.dt)
		for i in days5:
			print(i)
			print(i.dt)
		
	return render_template('forecast.html', days1=days1,days2=days2,days3=days3,days4=days4,days5=days5,days6=days6, city=city)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)