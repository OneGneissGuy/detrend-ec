# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 12:38:52 2018
script to read in conductivity data and correct for drift due to evaporation
@author: jsaracen
"""
import numpy as np
import pandas as pd
from scipy.signal import detrend
input_data_file = 'sc1000_data.csv'
#read the csv file into a pandas dataframe
data = pd.read_csv(input_data_file, index_col=[0])
#set the index to be a datetime index for time series operations
data.index = pd.to_datetime(data.index)
experiment_time = data.index[0] - data.index[-1]
hours = int(abs(experiment_time.total_seconds()/3600))
data.index = np.arange(1,hours+2)
data.index.name = u'Hour of Experiment'
#linearly detrend the data for effects of 
detrended = data.apply(detrend, type='linear')
#save the startingin intial conductivity values (no evaporation)
inital_values =  data.iloc[0]
# Add the intial value
detrended_plus_initial = detrended + inital_values
#save the output file to the same location as the input data 
detrended_plus_initial.to_csv(input_data_file.replace('.csv',
                                                      '_detrended.csv'))
#make some figures
ylab = u'Conductivity in microsiemens per centimeter (µS/cm)'
ax = data.plot.line(marker='o')
ax.set_ylabel(ylab)
ax.set_title('Raw')
ax = detrended_plus_initial.plot.line(marker='o')
ax.set_ylabel(ylab)
ax.set_title('Detrended')
