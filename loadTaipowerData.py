import mysql.connector
import json
import csv

# connet to mysql
connet = mysql.connector.connect(
	user="dm",
	password="dm", 
	host="127.0.0.1", 
	database="DM_hw0"
)
cursor = connet.cursor()
insertData = list()

# load Taipower data, json file, from 2016/09/27 - 2017/09/02.
with open("./data/Taipower/power.json") as data_file:    
    loadData = json.load(data_file)

# tempDate, consider to load data from a day to day.
tempDate = '2016-09-27'
northSupply = northUsage = centerSupply = centerUsage = southSupply = southUsage = eastSupply = eastUsage = 0.0

for i in range(len(loadData)):

	# cuase there is 2017-09-02 data in csv file, and the csv file is more accurate.
	if loadData[i]["create_date"]["$date"][:10] == "2017-09-02": break;

	tempDate = loadData[i]["create_date"]["$date"][:10]
	tempTime = loadData[i]["create_date"]["$date"][10:]
	northSupply = float(loadData[i]["regionData"]["northSupply"])
	northUsage = float(loadData[i]["regionData"]["northUsage"])
	centerSupply = float(loadData[i]["regionData"]["centerSupply"])
	centerUsage = float(loadData[i]["regionData"]["centerUsage"])
	southSupply = float(loadData[i]["regionData"]["southSupply"])
	southUsage = float(loadData[i]["regionData"]["southUsage"])
	eastSupply = float(loadData[i]["regionData"]["eastSupply"])
	eastUsage = float(loadData[i]["regionData"]["eastUsage"])

	insertData.append(tuple((
		tempDate, tempTime, northSupply, northUsage, centerSupply, centerUsage, southSupply, southUsage, eastSupply, eastUsage
	)))

# load Taipower data, csv file, from 2017/09/02 - 2017/09/23.
for i in range(2, 24):

	# cause the file does not exist.
	if i == 10: continue

	date = "2017-09-" + str(i)
	file = "./data/Taipower/" + date + ".csv"
	f = open(file, 'r')

	for row in csv.reader(f):
		northSupply = float(row[1])
		northUsage = float(row[2])
		centerSupply = float(row[3])
		centerUsage = float(row[4])
		southSupply = float(row[5])
		southUsage = float(row[6])
		eastSupply = float(row[7])
		eastUsage = float(row[8])

		insertData.append(tuple((
			date, row[0], northSupply, northUsage, centerSupply, centerUsage, southSupply, southUsage, eastSupply, eastUsage
		)))
	f.close()

# insert data to database.
insert = ("INSERT INTO `test` (date, time, northSupply, northUsage, centerSupply, centerUsage, southSupply, southUsage, eastSupply, eastUsage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
cursor.executemany(insert, insertData);
connet.commit()
cursor.close()

# close mysql connetion.
connet.close()
