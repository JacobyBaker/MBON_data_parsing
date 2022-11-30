#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
This script is to take a sipper metadata file from STOQS and parce it out and take the averages for each bottle so Marguerite can use them.

By: Jacoby Baker 11/29/22
'''


import os # to change directories
import pandas as pd # to manipulate the dataframe


os.getcwd()


# move to the directory with the data
os.chdir('/Users/jbaker/Documents/metadata/sipper')


# define the working directory
working_dir = '/Users/jbaker/Documents/metadata/sipper/'
print(working_dir)
# read in the file
df = pd.read_csv(working_dir + '202109_sipper.csv')



# make a blank dataframe
sip_means = pd.DataFrame({'bottle_name':[],'depth':[],'lat':[],'lon':[],'temp':[],'par':[],'chl':[],'sal':[]})

# get the individual bottle names so we can start parsing the data
bottles = df['measurement__instantpoint__activity__name'].drop_duplicates()
bottles

# identify the measurements we want averages for and separate based on the format
measurements1 = ['measurement__depth','measurement__geom.x','measurement__geom.y'] # these are in columns
measurements2 = ['temperature (degC)','PAR (umol/s/m2)','chlorophyll (ug/l)','salinity (psu)'] # these are in rows

# for each bottle, lets get the data we need!
for bottle in bottles:
    sip_bot = df.loc[(df['measurement__instantpoint__activity__name']==bottle)]
    # need to get means for measurements1 for each bottle, name them as variables to be able to add to the df
    num = sip_bot['measurement__instantpoint__activity__name']
    dep = sip_bot['measurement__depth'].mean()
    lat = sip_bot['measurement__geom.x'].mean()
    lon = sip_bot['measurement__geom.y'].mean()

    # for each measurement in the rows for each bottle, parse out each measurement and take the mean
    for measurement in measurements2:
        sip_bot_measurement = sip_bot.loc[(sip_bot['parameter__name'] == measurement)]
        sip1_measurement_mean = sip_bot_measurement['datavalue'].mean()

        if measurement == 'temperature (degC)':
            temp = sip1_measurement_mean
        if measurement == 'PAR (umol/s/m2)':
            par = sip1_measurement_mean
        if measurement == 'chlorophyll (ug/l)':
            chl = sip1_measurement_mean
        if measurement == 'salinity (psu)':
            sal = sip1_measurement_mean

    # assign the values into the dataframe
    sip_means.loc[len(sip_means.index)] = (bottle, dep, lat, lon, temp, par, chl, sal)

# make a bottle number column from the bottle name column
sip_means['bottle'] = sip_means.bottle_name.str.extract(r'(.*?)[ ](\d*)')[1]




# remove the index then save file
sip_means.set_index('bottle', inplace=True)

sip_means.to_csv(working_dir + '202109_sipper_means.csv')
