from time import time
import pandas as pd
import numpy as np
import random
import csv
import getData
import predictAlg

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

algorithmType = {
	0: "knn",
	1: "Naive Bayes",
	2: "Random Forest",
	3: "svm",

	4: "Bayesian regression",
	5: "Decision tree regression",
	6: "svr"
}

def setTTData(dataIndex, data):
	dataX = []
	dataY = []
	for i in dataIndex:
		dataX.append([i])
		dataY.append(data[i])

	return dataX, dataY


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

	f = open('./result/predict/result.csv', 'w')
	w = csv.writer(f)
	writeData = [
		['', 'Exact Value', '', ''], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], [], [], ['', '', ''], ['', '', ''], []
	]
	for i in algorithmType:
		writeData[0].append(algorithmType[i])
	for i in predictTime:
		index = i + 1 + i * 3
		print index
		writeData[index].append(predictTime[i])
		writeData[index].append('')
		writeData[index].append('')
		writeData[index].append("Predict Value")
		writeData[index+1].append("Predicting error percentage")
		writeData[index+2].append("Testing error percentage")

	"""
	Use 96 rows(27 days) to predict.
	Window will be slided 2 hour each time.
	traning data: 70% (96 * 0.7 = 67)
	testing data: 30% (96 * 0.3 = 29)
	"""
	realIndex = 96
	finalPredict = []
	finalTestingError = []
	finalPredictingError = []
	""" 7 algorithm """
	for i in range(7):
		finalPredict.append(np.array([]))
		finalTestingError.append(np.array([]))
		finalPredictingError.append(np.array([]))

	for i in range(1):
		randomDataIndex = random.sample(xrange(0 + i, 96 + i), 96)
		traningDataIndex = sorted(randomDataIndex[:67])
		testingDataIndex = sorted(randomDataIndex[67:96])

		""" reshape """
		tempData = [0] * 200
		for j in randomDataIndex:
			tempData[j] = round(northSupply[j % 12][j / 12], 1) * 10

		""" set traning/testing data """
		traningX, traningY = setTTData(traningDataIndex, tempData)
		testingX, testingY = setTTData(testingDataIndex, tempData)
		realAnswer = northSupply[(realIndex + i) % 12][(realIndex + i) / 12]

		print "Date: ", predictTime[i]
		print "Exact value: " + str(realAnswer) + '\n'

		for j in algorithmType:
			t0 = time()
			predict, testingError, predictingError = predictAlg.method(algorithmType[j], traningX, traningY, testingX, testingY, testingDataIndex, realAnswer)
			print("done in %0.3fs.\n" % (time() - t0))
			finalPredict[j] =  np.append(finalPredict[j], predict)
			finalTestingError[j] = np.append(finalTestingError[j], testingError)
			finalPredictingError[j] = np.append(finalPredictingError[j], predictingError)

		print "\n"


	w.writerows(writeData)
	f.close()
	#print np.average(finalPredictingError[3])
