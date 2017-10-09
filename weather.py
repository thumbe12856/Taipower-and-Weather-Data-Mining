import xml.etree.ElementTree
import time
import csv

def findMaxTemperature(area, city, cityIndex):
	fromDate = time.strptime('2016/10/01', "%Y/%m/%d")
	toDate = time.strptime('2017/07/01', "%Y/%m/%d")
	tempDate = '2016-10-01'
	MaxTemperature = -10000.0

	f = open('./result/weather/task2/2.c/' + area + '.csv', 'w')
	w = csv.writer(f)
	writeData = [
		[area, 'Date', 'Max Temperature']
	]

	# root -> dataset (root[7]) -> location Taipei (root[7][3])
	#	-> weatherElement (root[7][3][2]) -> find all time 
	for timeElement in root[7][cityIndex][2].findall('{urn:cwb:gov:tw:cwbcommon:0.1}time'):
		tempNowDate = time.strptime(timeElement[0].text[:10], "%Y-%m-%d")
		if(tempNowDate >= fromDate and tempNowDate <= toDate):
			if(tempDate != timeElement[0].text[:10]):
				writeData.append([city, tempDate, MaxTemperature])
				tempDate = timeElement[0].text[:10]
				MaxTemperature = -10000
			else:
				tempTemperature = float(timeElement[2][1][0].text)
				if(tempTemperature > MaxTemperature):
					MaxTemperature = tempTemperature

	w.writerows(writeData)
	f.close()


# get root of the xml file
root = xml.etree.ElementTree.parse('./data/weather/C-B0024-002.xml').getroot()

# Task 2.b
# find all locationName
# root -> dataset(root[7]) -> locationName(location[0])
for location in root[7]:
	print location[0].text

# Task 2.c
# Find the maximum temperature value for each day and each area, 
# 	(North , Center , South , East) from 2016/10/01 to 2017/06/30.
# North: Taipei, 466920, root[7][3]
# Center: Taitung, 467490, root[7][26]
# South: Kaohsiung, 467440, root[7][15]
# East: Taichung, 467490, root[7][17]

findMaxTemperature('North area', 'Taipei', 3)
findMaxTemperature('Center area', 'Taitung', 26)
findMaxTemperature('South area', 'Kaohsiung', 15)
findMaxTemperature('East area', 'Taichung', 17)
