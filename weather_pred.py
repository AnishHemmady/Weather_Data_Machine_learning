import pandas as pd
import numpy as np


def read_file():
	data=pd.read_csv("KININDIA168.csv")
	#dont know how this guy popped up had to delete this column :)
	df = data.drop('Unnamed: 0', 1)
	print(df)
	
read_file()