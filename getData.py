import numpy as np
import pandas as pd
import time
import numpy as np
import mysql.connector
import datetime
from datetime import timedelta, date

beforeStartDate = date(2016, 10, 20)
startDate = date(2016, 10, 20)
endDate = date(2016, 11, 15)

# get power data from mysql
def power():

	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	# SELECT * FROM `test` Where (test.date>= '2016-10-01' and test.date <= '2017-01-23') or (test.date>= '2017-04-20' and test.date <= '2017-06-30')
	query = ("SELECT * \
		FROM `test`\
		Where (test.date>='" + str(startDate) + "'and test.date <= '" + str(endDate) +"')")
		#Where (test.date>='" + str(startDate) + "'and test.date <= '2017-01-23') or (test.date>= '2017-04-20'\
		#and test.date <= '" + str(endDate) +"')")

	# morning: 6 ~ 9
	# afternoon: 11 ~ 14
	# night: 18 ~ 21
	cursor.execute(query)
	parseData = list()
	morning = 0
	afternoon = 4
	night = 8
	temp = [0] * (8 * 3 * 4 + 1)
	tempDate = startDate.strftime("%Y-%m-%d")

	for result in cursor:
		if(tempDate != result[1].strftime("%Y-%m-%d")):
			temp[8 * 3 * 4] = tempDate
			tempDate = result[1].strftime("%Y-%m-%d")
			parseData.append(temp)
			morning = 0
			afternoon = 4
			night = 8
			temp = [0] * (8 * 3 * 4 + 1)
		hour = result[2][1] + result[2][2]
		if(6 <= int(hour) and int(hour) <= 9):
			for i in range(8):
				temp[morning + 12 * i] = result[3 + i]
			morning = morning + 1

		elif(11 <= int(hour) and int(hour) <= 14):
			for i in range(8):
				temp[afternoon + 12 * i] = result[3 + i]
			afternoon = afternoon + 1

		elif(18 <= int(hour) and int(hour) <= 21):
			for i in range(8):
				temp[night + 12 * i] = result[3 + i]
			night = night + 1

	temp[8 * 3 * 4] = tempDate
	parseData.append(temp)

	powerDataDF = pd.DataFrame(parseData)

	# close connection
	connet.close()

	return powerDataDF

# get weather data
def weather(cityIndex, time, column):

	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	query = ("SELECT weather.date, weather.temperature \
		FROM `weather` \
		where ((weather.date>='" + str(startDate) + "'and weather.date <= '" + str(endDate) +"'))\
		and weather.cityIndex=" + str(cityIndex) + 
		" and weather.time >= '" + str(time['from']) + "' and weather.time <= '" + str(time['to']) + "'")
		#where ((weather.date>='" + str(startDate) + "'and weather.date <= '2017-01-23') or (weather.date>= '2017-04-20'\
		#and weather.date <= '" + str(endDate) +"'))\
	cursor.execute(query)
	date = list()
	value = list()
	tempDate = startDate.strftime("%Y-%m-%d")
	temp = list()

	for result in cursor:
		if(tempDate != result[0].strftime("%Y-%m-%d")):
			date.append(tempDate)
			value.append(temp)
			tempDate = result[0].strftime("%Y-%m-%d")
			temp = list()
		
		temp.append(result[1])
	value.append(temp)

	valueDF = pd.DataFrame(value, columns=[column+"1", column+"2", column+"3", column+"4"])
	# close connection
	connet.close()
	return valueDF
