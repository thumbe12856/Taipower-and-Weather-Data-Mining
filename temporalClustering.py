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

import getData

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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
powerDataDF = getData.power()

# date: powerDataDF[96]
# northSupply: powerDataDF.iloc[4*3 * 0 : 4*3 * 1]
# northUsage:  powerDataDF.iloc[4*3 * 1 : 4*3 * 2]
northSupply = powerDataDF.iloc[:,0:12]
northUsage  = powerDataDF.iloc[:,12:24]

# get temperature data
morningTemperature = getData.weather(3, morningTime, 'morning')
afternoonTemperature = getData.weather(3, afternoonTime, 'afternoon')
nightTemperature = getData.weather(3, nightTime, 'night')
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
