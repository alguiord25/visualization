#!/usr/bin/env python3

import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as tkr
import numpy as np

def plot_df(csv_file, x_name, y_name, title):
    headers = [x_name, y_name]
    df = pd.read_csv(csv_file, names = headers)

    print(df.dtypes)

    x = df[x_name]
    y = df[y_name]
    fig, ax = plt.subplots()
    plt.title(title)
    plt.xticks(rotation=-45,horizontalalignment='left')
    locator = tkr.MaxNLocator(nbins=12) 
    ax.xaxis.set_major_locator(locator)
    plt.subplots_adjust(bottom=0.21)

    plt.plot(x,y)
    plt.grid()
    print(df)


plot_df('19/08/18/99_T.csv','Date','Temp',"Temperature")
#plot_df('4_L.csv','Date','Light',"Light Intensity")
#plot_df('4_AH.csv','Date','AH',"Air Humidity")
#plot_df('4_T.csv','Date','Temp',"Temperature data")

plt.show()




