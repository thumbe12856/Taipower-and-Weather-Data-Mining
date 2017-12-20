import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

""" main """
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
print northSupply.size
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
use 96 rows(8 days) to predict
traning data: 70%
testing data: 30%
"""

