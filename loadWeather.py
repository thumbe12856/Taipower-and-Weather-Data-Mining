import mysql.connector
import xml.etree.ElementTree

def decodeChinese(text):
    try:
        unicode(text, 'utf-8')
        return unicode(text, 'utf-8')
    except TypeError:
        return text

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
	# root -> dataset(root[7]) -> locationName(location[0])
	for timeElement in root[7][cityIndex][2].findall('{urn:cwb:gov:tw:cwbcommon:0.1}time'):
		# tempNowDate = time.strptime(timeElement[0].text[:10], "%Y-%m-%d")
		date = timeElement[0].text[:10]
		time = timeElement[0].text[10:]
		temperature = float(timeElement[2][1][0].text)
		humidity = 0 if(timeElement[3][1][0].text == 'T') else float(timeElement[3][1][0].text)
		wind = 0 if(timeElement[4][1][0].text == 'T') else float(timeElement[4][1][0].text)
		precipitation = 0 if(timeElement[6][1][0].text == 'T') else float(timeElement[6][1][0].text)
		insertData.append(tuple((
			date, time, city, cityIndex, temperature, humidity, wind, precipitation
		)))
	insert = ("INSERT INTO `weather` (date, time, city, cityIndex, temperature, humidity, wind, precipitation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
	cursor.executemany(insert, insertData);
	connet.commit()
	cursor.close()	
	# close mysql connetion.
	connet.close()


root = xml.etree.ElementTree.parse('./data/weather/C-B0024-002.xml').getroot()

insertDataToDB('Taipei', 3)
insertDataToDB('Taitung', 26)
insertDataToDB('Kaohsiung', 15)
insertDataToDB('Taichung', 17)
