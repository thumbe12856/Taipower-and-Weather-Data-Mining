import csv
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn import datasets
from sklearn.cluster import DBSCAN
import itertools
import matplotlib.pyplot as plt
import itertools
import time
import numpy as np
import mysql.connector
import datetime
from datetime import timedelta, date

beforeStartDate = date(2016, 9, 30)
startDate = date(2016, 10, 1)
endDate = date(2017, 6, 30)

morningTime = {
	'from': ' 06:00',
	'to':   ' 09:00'
}

afternoonTime = {
	'from': ' 11:00',
	'to':   ' 14:00'
}

nightTime = {
	'from': ' 18:00',
	'to':   ' 21:00'
}

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

LABEL_COLOR_MAP = {
	0: 'r',
	1: 'g',
	2: 'b',
	3: 'black',
	4: 'magenta',
	5: 'cyan',
	6: 'yellow',
	7: 'brown',
	8: 'gray',
	9: 'olive',
	10: 'purple',
	11: '#885159',
	12: '#528881',
	13: '#bc4b4b',
	14: '#18392b',
	15: '#5a75ad',
	16: '#ff9000',
	17: '#a5d3a6'
}

# get location data
def getLocationData():
	file = "./data/location.csv"
	f = open(file, 'r')
	locations = list()
	swit = False
	for row in csv.reader(f):
		if(swit):
			row[3] = float(row[3])
			row[4] = float(row[4])
			locations.append(row)
		if(row[3] < 120):
			print row[1]
		swit = True
	f.close()
	return locations

# get power data from mysql
def getPowerData():

	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	# SELECT * FROM `test` Where test.date>= '2016-10-01' and test.date <= '2017-01-23' and test.date>= '2017-04-20' and test.date <= '2017-06-30'
	query = ("SELECT * \
		FROM `test`\
		Where (test.date>='" + str(startDate) + "'and test.date <= '2017-01-23') or (test.date>= '2017-04-20'\
		and test.date <= '" + str(endDate) +"')")

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
def getWeatherData(cityIndex, time, column):

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
		where ((weather.date>='" + str(startDate) + "'and weather.date <= '2017-01-23') or (weather.date>= '2017-04-20'\
		and weather.date <= '" + str(endDate) +"'))\
		and weather.cityIndex=" + str(cityIndex) + 
		" and weather.time >= '" + str(time['from']) + "' and weather.time <= '" + str(time['to']) + "'")
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

	valueDF = pd.DataFrame(value, columns=[column, column, column, column])
	# close connection
	connet.close()
	return valueDF

# pca
def pcaReduce(data):
	# n_components: [morning*4, afternoon*4, night*4] => [1 component]
	pca = PCA(n_components=1)

	# Fit and transform the data to the model
	pcaData = pca.fit_transform(data)
	print pca.explained_variance_ratio_
	pcaData = np.multiply(pcaData, 100)
	pcaData = np.floor(pcaData)

	return pcaData

# k-means
def kmeans(data):
	# n_clusters = summner and not summer
	kmeans_model = KMeans(n_clusters=2, random_state=1)
	distances = kmeans_model.fit_transform(data)
	labels = kmeans_model.labels_
	label_color = [LABEL_COLOR_MAP[l] for l in labels]

	return label_color


# main
# get north power data
powerDataDF = getPowerData()

# date: powerDataDF[96]
# northSupply: powerDataDF.iloc[4*3 * 0 : 4*3 * 1]
# northUsage:  powerDataDF.iloc[4*3 * 1 : 4*3 * 2]
northSupply = powerDataDF.iloc[:,0:12]
northUsage  = powerDataDF.iloc[:,12:24]

# get temperature data
morningTemperature = getWeatherData(3, morningTime, 'morning')
afternoonTemperature = getWeatherData(3, afternoonTime, 'afternoon')
nightTemperature = getWeatherData(3, nightTime, 'night')
temperature = pd.concat([morningTemperature, afternoonTemperature, nightTemperature], axis=1)

# pca
northSupplyPca = pcaReduce(northSupply)
northUsagePca  = pcaReduce(northUsage)
temperaturePca  = pcaReduce(temperature)


# kmeans
northSupplyLabelColor = kmeans(northSupplyPca)
northUsageLabelColor = kmeans(northSupplyPca)
temperatureLabelColor = kmeans(temperaturePca)

'''
# DBSCAN
northSupplyLabelColor = DBSCAN(eps = 5500, min_samples = 10).fit_predict(northSupplyPca)
northUsageLabelColor = DBSCAN(eps = 5500, min_samples = 10).fit_predict(northUsagePca)
temperatureLabelColor = DBSCAN(eps = 200, min_samples = 10).fit_predict(temperaturePca)
'''

plt.figure(1)
plt.scatter(powerDataDF[96], northSupplyPca, c=northSupplyLabelColor)

plt.figure(2)
plt.scatter(powerDataDF[96], northUsagePca, c=northUsageLabelColor)

plt.figure(3)
plt.scatter(powerDataDF[96], temperaturePca, c=temperatureLabelColor)
plt.show()
