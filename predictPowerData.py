from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
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

def setTTData(traningDataIndex, testingDataIndex, data):
	traningX = []
	traningY = []
	for i in traningDataIndex:
		traningX.append([i])
		traningY.append(data[i])

	testingX = []
	testingY = []
	for i in testingDataIndex:
		testingX.append([i])
		testingY.append(data[i])

	return traningX, traningY, testingX, testingY


""" knn algorithm to predict """
def knn(traningX, traningY, testingX, testingY):

	neigh = KNeighborsClassifier(n_neighbors=4)
	neigh.fit(traningX, traningY) 

	error = 0.0
	ii = 0
	for i in testingDataIndex:
		predict = neigh.predict([[i]])
		error += abs(predict[0] - testingY[ii]) / testingY[ii]
		ii = ii + 1
	error /= len(testingDataIndex)

	predict = neigh.predict([[97]]) / 10
	print "knn predict: " + str(round(predict[0], 1))
	print "knn testing error percentage: " + str(round(error * 100, 2)) + "%"
	print "knn predicting error percentage: " + str(round(abs(round(predict[0], 1) - realAnswer) / realAnswer * 100, 2)) + '%\n'

	return

def NaiveBayes(traningX, traningY, testingX, testingY):

	clf = GaussianNB()
	clf.fit(traningX, traningY) 

	error = 0.0
	ii = 0
	for i in testingDataIndex:
		predict = clf.predict([[i]])
		error += abs(predict[0] - testingY[ii]) / testingY[ii]
		ii = ii + 1
	error /= len(testingDataIndex)

	predict = clf.predict([[97]]) / 10
	print "Naive Bayes predict: " + str(round(predict[0], 1))
	print "Naive Bayes testing error percentage: " + str(round(error * 100, 2)) + "%"
	print "Naive Bayes predicting error percentage: " + str(round(abs(round(predict[0], 1) - realAnswer) / realAnswer * 100, 2)) + '%\n'

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
	realIndex = 96
	for i in range(1):
		randomDataIndex = random.sample(xrange(0 + i, 96 + i), 96)
		traningDataIndex = sorted(randomDataIndex[:67])
		testingDataIndex = sorted(randomDataIndex[67:96])

		""" reshape """
		tempData = [0] * 200
		for j in randomDataIndex:
			tempData[j] = round(northSupply[j % 12][j / 12], 1) * 10

		""" set traning/testing data """
		traningX, traningY, testingX, testingY = setTTData(traningDataIndex, testingDataIndex, tempData)
		realAnswer = northSupply[(realIndex + i) % 12][(realIndex + i) / 12]

		print "Date: ", predictTime[i]
		print "Exact value: " + str(realAnswer) + '\n'
		knn(traningX, traningY, testingX, testingY)
		NaiveBayes(traningX, traningY, testingX, testingY)

		print "\n"
