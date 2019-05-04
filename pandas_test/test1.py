#!/usr/bin/python3
from matplotlib import pyplot
from datetime import datetime,timedelta
#import csv
import pandas as pd
series = pd.read_csv('/home/pi/Documents/Repository/visualization/pandas_test//daily-min-temperatures.csv')
print(series.head())
series.plot()
#series.plot(style='k.')
#series.plot(kind='kde')
#pyplot.show()


now = datetime.now()
print(now)

ordinal = now.toordinal() 
print(ordinal)

datefromordinal = datetime.fromordinal(ordinal)
print(datefromordinal)

time = now-datefromordinal
print(time)

#seconds = timedelta(hours=time.hour,minutes=time.minute,seconds=time.second).total_seconds()

seconds = time.total_seconds()

print(seconds)
print(int(seconds))

index = ordinal + (int(seconds)/100000)
print(index)
#groups = series.groupby('A')
#years = pd.DataFrame()
#for name, group in groups:
#	years[name.year] = group.values
#years.plot(subplots=True, legend=False)
#pyplot.show()
