# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:29:11 2021

@author: celal.yanpar
"""
import wbdata
import datetime
from linear_regression import *

#get World Bank data
data_date = (datetime.datetime(2015, 1, 1), datetime.datetime(2019, 1, 1))
indicators = {"IC.BUS.DFRN.XQ": "doing_business", "NY.GDP.PCAP.PP.KD": "gdppc","SE.PRM.ENRR":"education level"}
df = pd.DataFrame(wbdata.get_dataframe(indicators,data_date=data_date ,convert_date=True))

#drop aggregated data and get only countries
df.drop(df.index[0:245], inplace=True)

#data preparing for linear regression model.
#exp_var = explanatory variable, cont_var= control variable
df = df.rename({'doing_business': 'target',"gdppc": "exp_var", "education level": "cont_var"}, axis=1)
df.reset_index(inplace=True)
df.set_index("country", inplace = True)
df = df.drop(columns= "date",axis=0)

#fill na values with country mean 
a = df.groupby(level=0).count()
missing_rows = a.index[(a['exp_var'] < 2 ) | (a["cont_var"] < 2)].tolist()
df = df.drop(missing_rows)
df['cont_var']= df['cont_var'].fillna(df.groupby(level = 0)['cont_var'].transform('mean'))

#write raw data to csv
df.to_csv("raw_data.csv")

try:
    regression_estimates, standard_errors, confidence_intervals = linear_regression(df)

except Exception as e: 
    print (e)