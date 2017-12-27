from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor

def method(alg, trainingX, trainingY, testingX, testingY, testingDataIndex, realAnswer):

	if(alg == "K Nearest Neighbor"): 
		""" K Nearest Neighbor algorithm to predict """
		clf = KNeighborsClassifier(n_neighbors=1)
	
	elif(alg == "Naive Bayes"):
		""" Naive Bayes algorithm Gaussian model to predict """
		clf = GaussianNB()
	
	elif(alg == "Random Forest"):
		""" Random Forest algorithm to predict """
		clf = RandomForestClassifier(max_depth=4, random_state=0)

	elif(alg == "Support vector machine classification"):
		""" Support vector machine classification algorithm to predict """
		clf = svm.SVC()

	elif(alg == "Bayesian regression"):
		""" Bayesian regression algorithm to predict """
		clf = linear_model.BayesianRidge()

	elif(alg == "Decision tree regression"):
		""" Decision tree regression algorithm to predict """
		clf = DecisionTreeRegressor()

	elif(alg == "Support vector machine regression"):
		""" Support vector machine regression algorithm to predict """
		clf = svm.SVR()

	else:
		print "error algorithm."
		return

	clf.fit(trainingX, trainingY) 

	error = 0.0
	ii = 0
	for i in testingDataIndex:
		predict = clf.predict([[i]])
		error += abs(predict[0] - testingY[ii]) / testingY[ii]
		ii = ii + 1
	error /= len(testingDataIndex)

	predict = clf.predict([[97]]) / 10
	predict = round(predict[0], 1)
	testingError = round(error * 100, 2)
	predictingError = round(abs(predict - realAnswer) / realAnswer * 100, 2)
	print alg + " predict: " + str(predict)
	print alg + " testing error percentage: " + str(testingError) + "%"
	print alg + " predicting error percentage: " + str(predictingError) + '%'

	return predict, testingError, predictingError
