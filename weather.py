import xml.etree.ElementTree
import time
import csv

def findAreaMaxTemperature(area, city, cityIndex):
	fromDate = time.strptime('2016/10/01', "%Y/%m/%d")
	toDate = time.strptime('2017/07/01', "%Y/%m/%d")
	tempDate = '2016-10-01'
	MaxTemperature = -10000.0

	f = open('./result/task2/2.c/' + area + '.csv', 'w')
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

	# write result to ./result/task2/2.c/{area}.csv.
	w.writerows(writeData)
	f.close()

def findAllAreaMaxAndMinTemperature():
	fromDate = time.strptime('2016/10/01', "%Y/%m/%d")
	toDate = time.strptime('2017/07/01', "%Y/%m/%d")
	MaxTemperature = -10000.0
	SecondMinTemperature = MinTemperature = 10000.0
	SecondMinTempCityName = SecondMinTempDate = MinTempCityName = MinTempDate = MaxTempCityName = MaxTempDate = ''

	for city in root[7]:
		for timeElement in city[2].findall('{urn:cwb:gov:tw:cwbcommon:0.1}time'):
			tempNowDate = time.strptime(timeElement[0].text[:10], "%Y-%m-%d")
			if(tempNowDate >= fromDate and tempNowDate <= toDate):
				tempTemperature = float(timeElement[2][1][0].text)
				if(tempTemperature > MaxTemperature):
					MaxTempCityName = city[0].text
					MaxTempDate = timeElement[0].text
					MaxTemperature = tempTemperature

				if(tempTemperature < MinTemperature):
					MinTempCityName = city[0].text
					MinTempDate = timeElement[0].text
					MinTemperature = tempTemperature

				# because the minimal value of temperature is unusual.
				if(tempTemperature < SecondMinTemperature and tempTemperature > -99.5):
					SecondMinTempCityName = city[0].text
					SecondMinTempDate = timeElement[0].text
					SecondMinTemperature = tempTemperature

	# write result to ./result/weather/task2/2.d/result.csv.
	f = open('./result/task2/2.d/result.csv', 'w')
	w = csv.writer(f)
	writeData = [
		['City', 'Date', 'Max Temperature'],
		[MaxTempCityName.encode('utf-8').strip(), MaxTempDate, MaxTemperature],
		['', ''],
		['City', 'Date', 'Min Temperature'],
		[MinTempCityName.encode('utf-8').strip(), MinTempDate, MinTemperature],
		['', ''],
		['City', 'Date', 'Second Min Temperature'],
		[SecondMinTempCityName.encode('utf-8').strip(), SecondMinTempDate, SecondMinTemperature]
	]
	w.writerows(writeData)
	f.close()

# main
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

findAreaMaxTemperature('North area', 'Taipei', 3)
findAreaMaxTemperature('Center area', 'Taitung', 26)
findAreaMaxTemperature('South area', 'Kaohsiung', 15)
findAreaMaxTemperature('East area', 'Taichung', 17)

# Task 2.d
findAllAreaMaxAndMinTemperature()
