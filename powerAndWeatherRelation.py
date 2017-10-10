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
	# value = list([0])
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

def getWeatherData(cityIndex):
	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	# value = list([0])
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


# main
# get power data
powerDate, powerSupply = getPowerData('northSupply')
powerDate, powerUsage = getPowerData('northUsage')

# get temperature data
weatherDate, taipeiTemperature = getWeatherData(3)

i = 0
for singleDate in daterange(startDate, endDate):
	tempDate = singleDate.strftime("%Y-%m-%d")
	taipeiTemperature[i] = taipeiTemperature[i] * 50
	if(weatherDate[i] != tempDate):
		print tempDate, ', ', i
		weatherDate = np.insert(weatherDate, i, tempDate)
		taipeiTemperature = np.insert(taipeiTemperature, i, 0)

	if(powerDate[i] != tempDate):
		powerDate = np.insert(powerDate, i, tempDate)
		powerSupply = np.insert(powerSupply, i, 0)
		powerUsage = np.insert(powerUsage, i, 0)
	i = i + 1;

plt.plot(weatherDate, taipeiTemperature, 'r--', weatherDate, powerSupply, 'bs', weatherDate, powerUsage, 'g^')
plt.show()
