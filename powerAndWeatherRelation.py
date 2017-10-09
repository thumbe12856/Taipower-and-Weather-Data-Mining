import xml.etree.ElementTree
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

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
	value = list()
	query = ("SELECT " + powerCategory + " FROM `test` ")
	cursor.execute(query)
	for result in cursor:
		value.append((result[0]))		
	# close connection
	connet.close()
	return value


# get temperature data
# get root of the xml file
root = xml.etree.ElementTree.parse('./data/weather/C-B0024-002.xml').getroot()

cityIndex = 3 # Taipei
temperature = list()
fromDateSwit = False
fromDate = time.strptime('2016/09/27', "%Y/%m/%d")
toDate = time.strptime('2017/09/23', "%Y/%m/%d")
tempDate = '2016-09-27'

# root -> dataset(root[7]) -> locationName(location[0])
for timeElement in root[7][cityIndex][2].findall('{urn:cwb:gov:tw:cwbcommon:0.1}time'):
	tempNowDate = time.strptime(timeElement[0].text[:10], "%Y-%m-%d")
	if(tempNowDate == fromDate):
		fromDateSwit = True
	if(fromDateSwit and tempNowDate <= toDate):
		temperature.append(float(timeElement[2][1][0].text))

# get power data
supply = getPowerData('northSupply')
usage = getPowerData('northUsage')

plt.plot(temperature, temperature, 'r--', supply, supply, 'bs', usage, usage, 'g^')
plt.show()
