import time
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import datetime
from datetime import timedelta, date

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
	query = ("SELECT test.date, AVG(test." + powerCategory + ") FROM `test` group by test.date")

	cursor.execute(query)
	for result in cursor:
		date = np.append(date, result[0].strftime('%Y-%m-%d'))
		value = np.append(value, result[1])

	# close connection
	connet.close()
	return date, value

def originalData(northSupply, northUsage, southSupply, southUsage):
	powerSupplyDistance = 0
	for i in range(powerDate.size):
		powerSupplyDistance += (northSupply[i] - southSupply[i]) * (northSupply[i] - southSupply[i])

	powerUsageDistance = 0
	# power usage comparation
	for i in range(powerDate.size):
		powerUsageDistance += (northUsage[i] - southUsage[i]) * (northUsage[i] - southUsage[i])

	print 'Before transformation:'
	print 'Distance between north and south power supply: ', powerSupplyDistance
	print 'Distance between north and south power usage: ', powerUsageDistance, '\n'


# main
# get north power data
powerDate, northSupply = getPowerData('northSupply')
powerDate, northUsage = getPowerData('northUsage')

# get south power data
powerDate, southSupply = getPowerData('southSupply')
powerDate, southUsage = getPowerData('southUsage')

# before use transformation, power supply comparation
originalData(northSupply, northUsage, southSupply, southUsage)
