import csv
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
import itertools

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

# K-means pre parsing
ori_cols = ['stationID', 'stationName', 'heigh', 'latitude', 'longitude', 'city', 'address', 'datafrom', 'removeDataDate', 'commit', 'originalStationID', 'newStationID', 'empty']
drop_cols = ['stationID', 'stationName', 'heigh', 'city', 'address', 'datafrom', 'removeDataDate', 'commit', 'originalStationID', 'newStationID', 'empty']
new_cols = ['latitude', 'longitude']
teams_df = pd.DataFrame(getLocationData(), columns = ori_cols)
df = teams_df.drop(drop_cols, axis=1)
data_attributes = df[new_cols]

# Create K-means model and determine euclidian distances for each data point
kmeans_model = KMeans(n_clusters=18, random_state=1)
distances = kmeans_model.fit_transform(data_attributes)

# Create scatter plot using labels from K-means model as color
labels = kmeans_model.labels_

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

label_color = [LABEL_COLOR_MAP[l] for l in labels]

#plt.scatter(df['latitude'], df['longitude'], c=label_color)
#plt.title('Kmeans Clusters')

#plt.show()

# DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import DBSCAN

y_pred = DBSCAN(eps = 0.5, min_samples = 10).fit_predict(data_attributes)
plt.scatter(data_attributes['latitude'], data_attributes['longitude'], c=y_pred)
plt.show()
