# -*- coding: utf-8 -*-
"""
Created on Wed Jan 4 00:45:30 2022

@author: celal.yanpar
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

def clear_missing_values(df):
    #according to cses documentation refused, dont know and missing values are eliminated
    df = df[df["D2021"] <=90]
    df = df[df["D2020"] <=5]
    df = df[df["D2004"] <=4]
    df = df[df["D2003"] <=9]
    df = df[df["D2002"] <=2]
    return df

def one_hot_encoder(df, encoding_columns):
   
    one_hot = pd.get_dummies(df[encoding_columns[0]])
    one_hot.rename(columns = {1:'male', 2:"female"}, inplace=True)
    # Drop column as it is now encoded
    df = df.drop(encoding_columns[0],axis = 1)
    # Join the encoded df
    df = df.join(one_hot)
    
    one_hot = pd.get_dummies(df[encoding_columns[1]])
    one_hot.rename(columns = {1:'EDU_1', 2:"EDU_2", 3:"EDU_3", 4:"EDU_4", 5:"EDU_5", 6:"EDU_6", 7:"EDU_7", 8:"EDU_8", 9:"EDU_9"}, inplace=True)
    # Drop column as it is now encoded
    df = df.drop(encoding_columns[1],axis = 1)
    # Join the encoded df
    df = df.join(one_hot)
    
    one_hot = pd.get_dummies(df[encoding_columns[2]])
    one_hot.rename(columns = {1:'married', 2:"widowed", 3:"divorced", 4:"single"}, inplace=True)
    # Drop column as it is now encoded
    df = df.drop(encoding_columns[2],axis = 1)
    # Join the encoded df
    df = df.join(one_hot)
    
    one_hot = pd.get_dummies(df[encoding_columns[3]])
    one_hot.rename(columns = {1:'low_income', 2:"second_income", 3:"third_income", 4:"fourth_income", 5: "highest income"}, inplace=True)
    # Drop column as it is now encoded
    df = df.drop(encoding_columns[3],axis = 1)
    # Join the encoded df
    df = df.join(one_hot)
    
    return df

def DimensionalityReduction(X_train,y_train,X_test): 
    lda = LDA(n_components=1)
    X_train = pd.DataFrame(lda.fit_transform(X_train,y_train))
    X_test = pd.DataFrame(lda.transform(X_test))
    return X_train, X_test
                    
def RandomForest(X_train,X_test,y_train,y_test):
    classifier = RandomForestClassifier(max_depth=5, random_state=0)#
    classifier.fit(X_train, y_train)
    preds1 = classifier.predict_proba(X_test)
    preds1 = preds1[:,1]
    auc_scr = roc_auc_score(y_test, preds1)
    print("AUC Score: {}".format(auc_scr))
    return preds1

def GradientBoosting(X_train,X_test,y_train,y_test):
    classifier = GradientBoostingClassifier()
    classifier.fit(X_train, y_train)
    preds2 = classifier.predict_proba(X_test)
    preds2 = preds2[:,1]
    auc_scr = roc_auc_score(y_test, preds2)
    print("AUC Score: {}".format(auc_scr))
    return preds2

def MultilayerPerceptron(X_train,X_test,y_train,y_test):
    classifier = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)
    classifier.fit(X_train, y_train)
    preds3 = classifier.predict_proba(X_test)
    preds3 = preds3[:,1]
    auc_scr = roc_auc_score(y_test, preds3)
    print("AUC Score: {}".format(auc_scr))
    return preds3


if __name__ == "__main__":
    
    df = pd.read_csv("cses4_cut.csv")
    #filter related column for analysis
    df = df[["D2002","D2003","D2004","age","D2020","D2021","voted"]]
    df = clear_missing_values(df)
    X = df[["D2002","D2003","D2004","age","D2020","D2021"]]
    encoding_columns = ["D2002","D2003","D2004","D2020"]
    X = one_hot_encoder(X, encoding_columns)
    X.rename(columns = {"D2021":'#in household'},inplace=True)
    y= pd.DataFrame(df["voted"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
    X_train, X_test = DimensionalityReduction(X_train, y_train, X_test)
    gb = pd.DataFrame(GradientBoosting(X_train,X_test,y_train,y_test))
    mlp = pd.DataFrame(MultilayerPerceptron(X_train,X_test,y_train,y_test))
    rf =pd.DataFrame(RandomForest(X_train,X_test,y_train,y_test))