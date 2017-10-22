import time
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import datetime
from datetime import timedelta, date

startDate = date(2016, 9, 27)
endDate = date(2017, 7, 3)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# get power data
def getPowerData(powerCategory):

	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	date = np.array([])
	value = np.array([])
	query = ("SELECT test.date, AVG(test." + powerCategory + ")\
		FROM `test`\
		Where test.date>='" + str(startDate) + "' and test.date <= '" + str(endDate) +"'\
		group by test.date")

	cursor.execute(query)
	for result in cursor:
		date = np.append(date, result[0].strftime('%Y-%m-%d'))
		value = np.append(value, result[1])

	# close connection
	connet.close()
	return date, value

# get weather data
def getWeatherData(cityIndex):

	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	date = np.array([])
	value = np.array([])
	query = ("SELECT weather.date, AVG(weather.temperature) \
		FROM `weather` \
		where weather.date>='" + str(startDate) + "' and weather.date <= '" + str(endDate) +"'\
		and weather.cityIndex=" + str(cityIndex) + 
		" group by weather.date")

	cursor.execute(query)
	for result in cursor:
		date = np.append(date, result[0].strftime('%Y-%m-%d'))
		value = np.append(value, result[1])

	# close connection
	connet.close()
	return date, value

# because there are some date that have no power data or weather data,
# so, this is to normalize.
def normalizeData(weatherDate, temperature, powerDate, powerSupply, powerUsage):
	i = 0
	for singleDate in daterange(startDate, endDate):
		tempDate = singleDate.strftime("%Y-%m-%d")
		temperature[i] = temperature[i] * 50

		# if weather has no data at the date, append 0 to data set
		if(weatherDate[i] != tempDate):
			print tempDate, ', ', i
			weatherDate = np.insert(weatherDate, i, tempDate)
			temperature = np.insert(temperature, i, 0)

		# if power has no data at the date, append 0 to data set
		if(powerDate[i] != tempDate):
			powerDate = np.insert(powerDate, i, tempDate)
			powerSupply = np.insert(powerSupply, i, 0)
			powerUsage = np.insert(powerUsage, i, 0)

		i = i + 1;

	return weatherDate, temperature, powerDate, powerSupply, powerUsage

def drawCurve(cityIndex, area):
	# get power data
	powerDate, powerSupply = getPowerData(area + 'Supply')
	powerDate, powerUsage = getPowerData(area + 'Usage')

	# get temperature data
	weatherDate, temperature = getWeatherData(cityIndex)

	# normalize the data
	weatherDate, temperature, powerDate, powerSupply, powerUsage = \
		normalizeData(weatherDate, temperature, powerDate, powerSupply, powerUsage)

	# draw curve
	plt.plot(weatherDate, temperature, 'r-', weatherDate, powerSupply, 'b-', weatherDate, powerUsage, 'g-')
	plt.show()


# main
# North: Taipei, 466920, [3]
drawCurve(3, 'north')

# Center: Taitung, 467490, [26]
drawCurve(26, 'center')

# South: Kaohsiung, 467440, [15]
drawCurve(15, 'south')

# East: Taichung, 467490, [17]
drawCurve(17, 'east')
