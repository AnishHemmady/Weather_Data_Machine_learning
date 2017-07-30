import pandas as pd
import numpy as np
from dateutil import parser, rrule

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
	print(finl_data.head())
	
read_file()