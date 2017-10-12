import mysql.connector
import xml.etree.ElementTree

def insertDataToDB(city, cityIndex):
	# connet to mysql
	connet = mysql.connector.connect(
		user="dm",
		password="dm", 
		host="127.0.0.1", 
		database="DM_hw0"
	)
	cursor = connet.cursor()
	insertData = list()
	root = xml.etree.ElementTree.parse('./data/weather/C-B0024-002.xml').getroot()
	
	# root -> dataset(root[7]) -> locationName(location[0])
	for timeElement in root[7][cityIndex][2].findall('{urn:cwb:gov:tw:cwbcommon:0.1}time'):

		# tempNowDate = time.strptime(timeElement[0].text[:10], "%Y-%m-%d")
		date = timeElement[0].text[:10]
		time = timeElement[0].text[10:]
		temperature = float(timeElement[2][1][0].text)
		insertData.append(tuple((
			date, time, city, cityIndex, temperature
		)))
	insert = ("INSERT INTO `weather` (date, time, city, cityIndex, temperature) VALUES (%s, %s, %s, %s, %s)")
	cursor.executemany(insert, insertData);
	connet.commit()
	cursor.close()
	
	# close mysql connetion.
	connet.close()


insertDataToDB('Taipei', 3)
insertDataToDB('Taitung', 26)
insertDataToDB('Kaohsiung', 15)
insertDataToDB('Taichung', 17)
