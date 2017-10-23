import time
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import datetime
from datetime import timedelta, date
import apyori, shutil, os
from apyori import apriori
from apyori import dump_as_json
import pandas as pd
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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
# so, remove the data from another side.
def normalizeData(weatherDate, temperature, powerDate, powerSupply, powerUsage):
	i = 0
	swit = False
	for singleDate in daterange(startDate, endDate):
		tempDate = singleDate.strftime("%Y-%m-%d")

		# if weather has no data at the date, remove power data at the date.
		if(weatherDate[i] != tempDate and powerDate[i] == tempDate):
			powerDate = np.delete(powerDate, i)
			powerSupply = np.delete(powerSupply, i)
			powerUsage = np.delete(powerUsage, i)
			swit = True

		# if power has no data at the date, remove weather data at the date.
		elif(powerDate[i] != tempDate and weatherDate[i] == tempDate):
			weatherDate = np.delete(weatherDate, i)
			temperature = np.delete(temperature, i)
			swit = True

		if(swit == False):
			i = i + 1

	return weatherDate, temperature, powerDate, powerSupply, powerUsage

# set data to transcaction list 
def setData(cityIndex, area, tempDiscretization, powerDiscretization):
	# get power data
	powerDate, powerSupply = getPowerData(area + 'Supply')
	powerDate, powerUsage = getPowerData(area + 'Usage')

	# get temperature data
	weatherDate, temperature = getWeatherData(cityIndex)

	# normalize the data
	weatherDate, temperature, powerDate, powerSupply, powerUsage = \
		normalizeData(weatherDate, temperature, powerDate, powerSupply, powerUsage)

	# discretization
	print 'discretization:'
	print '	temperature:', tempDiscretization
	print '	power:', powerDiscretization
	temperature = np.multiply(np.divide(temperature, tempDiscretization).astype(int), tempDiscretization)
	powerSupply = np.multiply(np.divide(powerSupply, powerDiscretization).astype(int), powerDiscretization)
	powerUsage = np.multiply(np.divide(powerUsage, powerDiscretization).astype(int), powerDiscretization * 10)

	print 'temperature unique data length: ', np.unique(temperature).size, ', min value:', np.min(temperature), ', max value:', np.max(temperature)
	print 'powerSupply unique data length: ', np.unique(powerSupply).size, ', min value:', np.min(powerSupply), ', max value:', np.max(powerSupply)
	print 'powerUsage unique data length: ', np.unique(powerUsage).size, ', min value:', np.min(powerUsage), ', max value:', np.max(powerUsage)
	print '\n'

	transactions = list()
	for i in range(temperature.size):
		transactions.append(tuple((
			temperature[i], powerSupply[i], powerUsage[i]
		)))

	print 'transactions length: ', len(transactions)
	print 'transactions: \n['
	for i in range(len(transactions)):
		print transactions[i], ', ',
		if((i+1) % 8 == 0):
			print
	print ']\n'

	return transactions

# Apriori alg
def printAprioriResult(transactions, support, confidence):
	
	# Apriori algorithm
	print 'Apriori algorithm:'
	print 'min_support: ', support
	results = list(apriori(transactions, min_support = support, min_confidence = confidence))
	results_df = pd.DataFrame()

	output = []
	for RelationRecord in results:
	    o = StringIO()
	    dump_as_json(RelationRecord, o)
	    output.append(json.loads(o.getvalue()))
	data_df = pd.DataFrame(output)

	print '\nfrequent item set:'
	for i in range(data_df['items'].size):
		print data_df['items'][i],',',

	print '\n\n[items],  [ordered_statistics],																			support'
	for i in range(data_df['items'].size):
		print data_df['items'][i], ',', data_df.ordered_statistics[i], ',', data_df.support[i]

	print '\nRules:'
	for i in range(data_df['items'].size):
		if(len(data_df.ordered_statistics[i]) > 1):
			for j in range(len(data_df.ordered_statistics[i])):
				# [6] -> [17], confidence: 0.6875, suport: 0.112244897959
				temp = data_df.ordered_statistics[i][j]
				print temp['items_base'], '->', temp['items_add'], ', confidence:', temp['confidence'], ', support:', data_df.support[i]


# main
# North: Taipei, 466920, [3]
print 'Location: Taipei'
transactions = setData(3, 'north', 5, 50)
printAprioriResult(transactions, 0.04, 0.1)

'''
# Center: Taichung, 467490, [26]
print 'Location: Taichung'
transactions = setData(26, 'center', 1, 10)
printResult(transactions)


# South: Kaohsiung, 467440, [15]
print 'Location: Kaohsiung'
transactions = setData(15, 'south', 1, 10)
printResult(transactions)


# East: Taitung, 467490, [17]
print 'Location: Taitung'
transactions = setData(17, 'east', 1, 10)
printResult(transactions)
'''
