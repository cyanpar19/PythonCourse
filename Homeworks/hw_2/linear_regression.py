# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:15:42 2021

@author: celal.yanpar
"""
import pandas as pd
import numpy as np

def displayText():
    print("Hello!")

def linear_regression(df):
    
    if isinstance(df, pd.DataFrame): # to check input as dataframe
        must_have_columns = ["target","exp_var", "cont_var"]
        
        #to check all required columns are provided
        if list(df.columns.values) == must_have_columns: 
            # to check column types are float rather than others
            if (df.target.dtypes =="float64" and df.exp_var.dtypes =="float64" and df.cont_var.dtypes =="float64"):
                
                #drop NA rows
                df= df.dropna(axis=0)
                
                #partition to feature and target sets
                X = df.drop(["target"], axis=1)
                X["constant"] = 1
                Y = pd.DataFrame(data=df["target"])
                
                #(X'X)^-1X'y;
                coefficients = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(Y)
                
                #find predictions
                Y_predicts = X.dot(coefficients)
                Y_predicts.columns = ["target"]
                
                error = Y-Y_predicts
                k=len(X.columns)
                n=len(X.index)
                #sigma^2 = (e'e)/(n-k-1)
                var_e = (error.transpose().dot(error)) / (n  - k - 1)
                #sigma^2(X'X)^1
                var_bb = var_e.iloc[0,0]*(np.linalg.inv(X.transpose().dot(X)))
                
                std_errors=[]
                confidences = []
                
                for k_ in range(k):
                    standard_error = var_bb[k_, k_] ** 0.5
                    std_errors.append(standard_error)
                
                #calculate confidence interval's upper and lower bound according to column order
                for i in range(k):
                    confidence_lower = coefficients[i,0] - 1.96 * std_errors[i]
                    confidence_upper = coefficients[i,0] + 1.96 * std_errors[i]
                    confidences.append(confidence_lower)
                    confidences.append(confidence_upper)
                
                return coefficients, std_errors, confidences  
            else:
             print("Input DataFrame columns must be float64 as type")
             return None   
        else:
            print("Input dataFrame must have, target, exp_var and cont_var columns")
            return None
    else:
        print("Input value must be pandas DataFrame")
        return None

