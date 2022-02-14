# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 13:53:38 2022

@author: philip.moffatt
"""

# conda install -c conda-forge ulmo - this takes ~30sec to run
# issues? go here https://ulmo.readthedocs.io/en/latest/
# similar tutorial steps http://earthpy.org/ulmo.html

import ulmo
from datetime import datetime
import numpy as np
import pandas
import matplotlib.pyplot as plt

# Call for catalog for different services; can use a bounding box to look at particular areas
# (min_longitude, min_latitude,max_longitude, and max_latitude) with these values in decimal degrees
# Chapter 5 of the ulmo documentation dives into each API and how to pull from it. 
# here I use the coordinates roughly for the PNW; CUSAHSI are water related products/climate change data (type-list)
ulmo.cuahsi.his_central.get_services(bbox = (-124.0, 42.0, -116.0, 48.0) )

# National Climatic Data Center Global Historical Climate Network - Daily dataset
# st = station table, pulled for all the US stations here
st = ulmo.ncdc.ghcn_daily.get_stations(country='US', as_dataframe=True)

# check the table out a bit; you could search this table by state, elevation, etc
st.head()

# go here to see all the stations for the network - serval ways to find stations here. 
# https://www.ncdc.noaa.gov/cdo-web/

# here is the daily data call using ulmo tool; this may take ~30sec to run

# the data is in mm. Check here for documentation - https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf
tx = ulmo.ncdc.ghcn_daily.get_data('USC00412679', as_dataframe=True)
tx
p1 = tx['PRCP'].copy()
p1.head()
# Lets grab Washington data for comparison to Texas
wa = ulmo.ncdc.ghcn_daily.get_data('USS0020B02S', as_dataframe=True)
wa
p2 = wa['PRCP'].copy()
p2.head()

# take a look at the time series plot
plt.figure()
p1['value']['1890':'2022'].plot()

# pandas makes sampling the data at different frequencies a snap!
# documentation on this method - https://www.geeksforgeeks.org/python-pandas-dataframe-resample/
# W : weekly frequency
# M : month end frequency
# SM : semi-month end frequency (15th and end of month)
# Q : quarter end frequency

# run these two lines together for a look at the last 30years
plt.figure()
p1['1990':'2020'].value.resample('A').plot()
plt.title('Annual precipitation in Southwestern Texas')

# a look at the last 30years
plt.figure()
p2['1990':'2020'].value.resample('A').plot()
plt.title('Annual precipitation in Central Washington')

# =============================================================================
# From EarthPY Tutorials - http://earthpy.org/
# Let's pull data for the Artic Oscillation and see if Punxsutawney Phil was 
# likely to be correct this year - correct 50% of the last 10years
# AO index is published by NOAA and is an indicator for how far cold air 
# pushes into lower latitudes bringing joy and winter blasts.
# here's documentation on AO https://www.ncdc.noaa.gov/teleconnections/ao/
# =============================================================================
# Packages necessary for the below exercise
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
pd.set_option('display.max_rows',15) # this limit maximum numbers of rows

# reach out to the API with cURL command; documentation https://developer.ibm.com/articles/what-is-curl-command/
# monthly index data from NOAA
!curl http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii >> 'monthly.ao.index.b50.current.ascii'

# open the file up with numpy
ao = np.loadtxt('/Users/philipmoffatt/Dropbox/Python/Climate Data Talk/monthly_prcp.csv', delimiter=',')
# what is this thing?
# it has 3 columns; they appear to be year, month, index value (when positive we are happy, if negative we are cold)
ao[0:2]
ao.shape

# convert this dataset to a time series 
# set up a range of dates that match the ao file!
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')
dates
# nice should be same length as ao!
# Now we make the time series and use dates as the index
AO = Series(ao[:,2], index=dates)

# look at it
plt.figure()
AO.plot()
plt.title('Arctic Oscillation')

# how about since I have been looking at the weather
plt.figure()
AO['1990':'2022'].plot()
plt.title('Arctic Oscillation - last 30 yrs')

# that does not appear to say anythin about 1996, 1999 snow accumulation, what's new
plt.figure()
AO['2021': '2022'].plot()
plt.title('Arctic Oscillation - recently')

# when were the most negative/pos years?
plt.figure()
AO[AO < -3].plot(kind='barh')
plt.title('Arctic Oscillation - Intense Negative Months')

plt.figure()
AO[AO > +3].plot(kind='barh')
plt.title('Arctic Oscillation - Intense Postive Months')

# really simply basic statistics
AO.mean()
AO.min() # saw this was Feb 2010
AO.describe()

# Using the resample method again - nice and quick method
AO_m = AO.resample("A").mean()
plt.figure()
AO_m.plot(style='r--')
plt.title('Arctic Oscillation - Annual Mean')

AO_md = AO.resample("A").median()
plt.figure()
AO_md.plot()
plt.title('Arctic Oscillation - Annual Median')

# this phase stuff seems to persist for clumps of time beyond 1 yr
# what's the biggest/smallest value every 3-years
AO_3y = AO.resample("3A").apply(np.max)
plt.figure()
AO_3y.plot()
plt.title('Arctic Oscillation - 3yr Max Values')

AO_3y = AO.resample("3A").apply(np.min)
plt.figure()
AO_3y.plot()
plt.title('Arctic Oscillation - 3yr Min Values')

# do mulitple plots of interest at one time
AO_mm = AO.resample("3A").apply(['mean', np.min, np.max])
plt.figure()
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()
plt.title('Arctic Oscillation - Descriptive Stats')

# use pandas rolling calculations
plt.figure()
AO.rolling(window=12, center=False).mean().plot(style='-g')
plt.title('Arctic Oscillation - Rolling Annual Mean')

plt.figure()
AO.rolling(window=12, center=False).var().plot(style='-g')
plt.title('Arctic Oscillation - Rolling Annual Variance')


# Make a money descriptive timeseries plot
# set figure size
plt.figure( figsize = ( 12, 5))
  
# plot a simple time series plot
AO.plot(style= 'y-')

# plot using rolling average
AO.rolling(window=12, center=False).mean().plot(style='b--')

plt.ylabel('Arctic Oscillation Index')
plt.title('Arctic Oscillation NOAA - Historical Record')






