# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:28:21 2021

@author: celal.yanpar
"""

from linear_regression import *
import pandas as pd

df  = pd.read_csv("raw_data.csv")
df.drop('country', axis=1, inplace=True)

#test:1 datatype test
df1 = "test"
try:
    regression_estimates, standard_errors, confidence_intervals = linear_regression(df1)
    print("test 1 passed")

except Exception as e: 
     print (e)
     print("test 1 fail")
     
#test:2 string value in column test
df2 = df
df2.iloc[0,2] = "testtest"

try:
    regression_estimates, standard_errors, confidence_intervals = linear_regression(df2)
    print("test 1 passed")

except Exception as e: 
     print (e)
     print("test 2 fail")
     
#test3: missing column test
df3= df.drop('target', axis=1, inplace=True)

try:
    regression_estimates, standard_errors, confidence_intervals = linear_regression(df3)
    print("test 3 passed")

except Exception as e: 
     print (e)
     print("test 3 fail")
