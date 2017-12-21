from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import random
import getData

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

predictTime = {
	0: '2016-10-28 06:00',
	1: '2016-10-28 07:00',
	2: '2016-10-28 08:00',
	3: '2016-10-28 09:00',
	4: '2016-10-28 11:00',
	5: '2016-10-28 12:00'
}


""" knn algorithm to predict """
def knn(traningDataIndex, testingDataIndex):

	traningX = []
	traningY = []
	for i in traningDataIndex:
		traningX.append([i])
		traningY.append(round(northSupply[i % 12][i / 12], 1) * 10)

	testingX = []
	testingY = []
	for i in testingDataIndex:
		testingX.append([i])
		testingY.append(round(northSupply[i % 12][i / 12], 1) * 10)

	neigh = KNeighborsClassifier(n_neighbors=3)
	neigh.fit(traningX, traningY) 

	error = 0.0
	ii = 0
	for i in testingDataIndex:
		predict = neigh.predict([[i]])
		error += abs(predict[0] - testingY[ii]) / testingY[ii]
		ii = ii + 1
	error /= len(testingDataIndex)
	print "knn error percentage: " + str(round(error * 100, 2)) + "%"

	predict = neigh.predict([[97]]) / 10
	print "knn predict: ", round(predict[0], 1)

	return


""" main """
if __name__ == "__main__":

	""" get north power data """
	powerDataDF = getData.power()

	"""
	 12 rows per day, each row:
	 morning: 06:00 ~ 09:00
	 afternoon: 11:00 ~ 14:00
	 night: 18:00 ~ 21:00

	 data format:
	 	powerDataDF['2016-10-01']['morning 06:00']
	 	powerDataDF['2016-10-01']['morning 07:00']
	 	...
	 	powerDataDF['2016-10-01']['night 21:00']
	"""
	northSupply = powerDataDF.iloc[:, 0:12]
	# northUsage  = powerDataDF.iloc[:,12:24]


	"""
	 get temperature data
	 data format:
		Temperature['2016-10-01']['morning 06:00']
	 	Temperature['2016-10-01']['morning 07:00']
	 	...
	 	Temperature['2016-10-01']['night 21:00']
	"""
	morningTemperature = getData.weather(3, morningTime, 'morning')
	afternoonTemperature = getData.weather(3, afternoonTime, 'afternoon')
	nightTemperature = getData.weather(3, nightTime, 'night')
	temperature = pd.concat([morningTemperature, afternoonTemperature, nightTemperature], axis=1)


	"""
	Use 96 rows(27 days) to predict.
	Window will be slided 2 hour each time.
	traning data: 70% (96 * 0.7 = 67)
	testing data: 30% (96 * 0.3 = 29)
	"""
	for i in range(6):
		randomDataIndex = random.sample(xrange(0 + i, 96 + i), 96)
		traningDataIndex = sorted(randomDataIndex[:67])
		testingDataIndex = sorted(randomDataIndex[67:96])

		print "Date: ", predictTime[i]
		knn(traningDataIndex, testingDataIndex)

		print "\n"
