import time
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from scipy import signal
from scipy.signal import lfilter

# get power data from mysql
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

# print original power data distance
def printDistance(northSupply, northUsage, southSupply, southUsage):
	powerSupplyDistance = 0
	for i in range(northSupply.size):
		powerSupplyDistance += (northSupply[i] - southSupply[i]) * (northSupply[i] - southSupply[i])

	powerUsageDistance = 0
	# power usage comparation
	for i in range(northUsage.size):
		powerUsageDistance += (northUsage[i] - southUsage[i]) * (northUsage[i] - southUsage[i])

	return powerSupplyDistance, powerUsageDistance

# transform data by mean
def meanTransformation(supply, usage):
	supply = np.subtract(supply, supply.mean())
	usage = np.subtract(usage, usage.mean())

	return supply, usage

# transform data by detrend
def amplitudeScalingTransformation(supply, usage):
	supply = np.subtract(supply, supply.mean()) / np.std(supply)
	usage = np.subtract(usage, usage.mean()) / np.std(usage)

	return supply, usage

def detrendTransformation(supply, usage):
	supply = signal.detrend(supply)
	usage = signal.detrend(usage)

	return supply, usage

def noiseReductionTransformation(supply, usage):
	b = [1.0 / supply.size] * supply.size
	a = 1
	supply = lfilter(b, a, supply)

	b = [1.0 / usage.size] * usage.size
	usage = lfilter(b, a, usage)

	return supply, usage


# main
# get north power data
powerDate, northSupply = getPowerData('northSupply')
powerDate, northUsage = getPowerData('northUsage')

# get south power data
powerDate, southSupply = getPowerData('southSupply')
powerDate, southUsage = getPowerData('southUsage')

# original power supply and usage data comparation
powerSupplyDistance, powerUsageDistance = printDistance(northSupply, northUsage, southSupply, southUsage)
print 'original data:'
print 'Distance between north and south power supply: ', powerSupplyDistance
print 'Distance between north and south power usage: ', powerUsageDistance, '\n'


# Offset transformation
meanTransNorthSupply, meanTransNorthUsage = meanTransformation(northSupply, northUsage)
meanTransSouthSupply, meanTransSouthUsage = meanTransformation(southSupply, southUsage)

powerSupplyDistance, powerUsageDistance = printDistance(meanTransNorthSupply, meanTransNorthUsage, meanTransSouthSupply, meanTransSouthUsage)
print 'After offset transformation:'
print 'Distance between north and south power supply: ', powerSupplyDistance
print 'Distance between north and south power usage: ', powerUsageDistance, '\n'


# Amplitude Scaling transformation
asTransNorthSupply, asTransNorthUsage = amplitudeScalingTransformation(northSupply, northUsage)
asTransSouthSupply, asTransSouthUsage = amplitudeScalingTransformation(southSupply, southUsage)

powerSupplyDistance, powerUsageDistance = printDistance(asTransNorthSupply, asTransNorthUsage, asTransSouthSupply, asTransSouthUsage)
print 'After amplitude scaling transformation:'
print 'Distance between north and south power supply: ', powerSupplyDistance
print 'Distance between north and south power usage: ', powerUsageDistance, '\n'


# Linear Trend Removal transformation
detrendTransNorthSupply, detrendTransNorthUsage = detrendTransformation(northSupply, northUsage)
detrendTransSouthSupply, detrendTransSouthUsage = detrendTransformation(southSupply, southUsage)

powerSupplyDistance, powerUsageDistance = printDistance(detrendTransNorthSupply, detrendTransNorthUsage, detrendTransSouthSupply, detrendTransSouthUsage)
print 'After linear trend removal transformation:'
print 'Distance between north and south power supply: ', powerSupplyDistance
print 'Distance between north and south power usage: ', powerUsageDistance, '\n'


# Noise Reduction transformation
nrTransNorthSupply, nrTransNorthUsage = noiseReductionTransformation(northSupply, northUsage)
nrTransSouthSupply, nrTransSouthUsage = noiseReductionTransformation(southSupply, southUsage)

powerSupplyDistance, powerUsageDistance = printDistance(nrTransNorthSupply, nrTransNorthUsage, nrTransSouthSupply, nrTransSouthUsage)
print 'After noise reduction transformation:'
print 'Distance between north and south power supply: ', powerSupplyDistance
print 'Distance between north and south power usage: ', powerUsageDistance, '\n'
