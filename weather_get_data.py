import requests
import pandas as pd
import time
from datetime import datetime,time,date
from dateutil import parser, rrule
import io
#station="KININDIA168"
def get_data(station,day,month,year):
	url = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID={station}&day={day}&month={month}&year={year}&graphspan=day&format=1"
	full_url = url.format(station=station, day=day, month=month, year=year)
	response = requests.get(full_url)
	data = response.text
	data=data.replace('<br>','')
	try:
		df=pd.read_csv(io.StringIO(data),index_col=False)
		df['station']=station
		#print(df)
	except Exception as e:
		print("error in connecting")
	return df
	
start_date="2016-07-01"
end_date="2017-07-25"
start = parser.parse(start_date)
end = parser.parse(end_date)
dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))
stations=["KININDIA168","KININDIA94"]
wait_time=10
data={}
for station in stations:
	print("Working on {}".format(station))
	data[station]=[]
	for date in dates:
		if date.day%20==0:
			print("Working on {} for date {}".format(station,date))
		finished=False
		while finished==False:
			try:
				weather_data=get_data(station,date.day,date.month,date.year)
				finished=True
			except Exception as e:
				print("Connection error please retry")
		data[station].append(weather_data)
	pd.concat(data[station]).to_csv("{}.csv".format(station))
				




