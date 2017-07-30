import pandas as pd
import numpy as np
from dateutil import parser, rrule
from matplotlib import pyplot as plt
def read_file():
	data=pd.read_csv("KININDIA168.csv")
	#dont know how this guy popped up had to delete this column :)
	df = data.drop('Unnamed: 0', 1)
	#print(df)
	#print(df.columns.values)
	df['temp']=df['TemperatureF'].astype(float)
	df['rain']=df['HourlyPrecipIn'].astype(float)
	df['total_rain']=df['dailyrainin'].astype(float)
	df['date']=df['DateUTC'].apply(parser.parse)
	df['himidity']=df['Humidity'].astype(float)
	df['wind_direction']=df['WindDirectionDegrees']
	df['wind_speed']=df['WindSpeedMPH']
	df=df.drop(['TemperatureF','HourlyPrecipIn','dailyrainin','DateUTC','Humidity','WindDirectionDegrees','WindSpeedMPH'],1)
	#print(df)
	finl_data=df.loc[:,['date','station','temp','rain','total_rain','humidity','wind_speed']]
	
	'''val=(finl_data['rain']<-500)
	print(val)
	if(finl_data['rain']<-500).sum()>10:
		print("messed up")'''	
	finl_data=finl_data[finl_data['rain']>-500]
	finl_data['day']=finl_data['date'].apply(lambda x:x.date())
	finl_data['time_of_day']=finl_data['date'].apply(lambda x:x.time())
	finl_data['day_of_week']=finl_data['date'].apply(lambda x:x.weekday())
	finl_data['hour_of_day']=finl_data['time_of_day'].apply(lambda x:x.hour)
	finl_data['month']=finl_data['date'].apply(lambda x:x.month)
	finl_data['raining']=finl_data['rain']>0.0
	rainy_days=finl_data.groupby(['day']).agg({"rain":{"rain":lambda x:(x>0.0).any(),"rain_amount":"sum"},"total_rain": {"total_rain": "max"}})
	rainy_days.reset_index(drop=False,inplace=True)
	rainy_days.rename(columns={"":"date"},inplace=True)
	rainy_days.columns=rainy_days.columns.droplevel(level=0)
	rainy_days['rain']=rainy_days['rain'].astype(bool)
	#rainy_days.loc[(rainy_days['rain_amount']<0.0),'rain_amount']=0.0
	#rainy_days.loc[(rainy_days['total_rain']<0.0),'total_rain']=0.0
	
	tempry=finl_data.groupby(["day","hour_of_day"])["raining"].any()
	tempry=tempry.groupby(level=[0]).sum().reset_index()
	tempry.rename(columns={'raining': 'hours_raining'}, inplace=True)
	tempry['day'] = tempry['day'].apply(lambda x: x.to_datetime().date())
	rainy_days = rainy_days.merge(tempry, left_on='date', right_on='day', how='left')
	rainy_days.drop('day', axis=1, inplace=True)
	print(rainy_days.tail())
	

	import calmap

	temp = rainy_days.copy().set_index(pd.DatetimeIndex(rainy_days['date']))
	#temp.set_index('date', inplace=True)
	fig, ax = calmap.calendarplot(temp['hours_raining'],fig_kws={"figsize":(15,2)})
	plt.title("Hours raining")
	plt.show()
	
read_file()