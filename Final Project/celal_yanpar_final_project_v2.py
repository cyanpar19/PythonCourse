# -*- coding: utf-8 -*-
"""
Created on Wed Jan 6 00:15:29 2022

@author: celal.yanpar

CSSM 502 Final Project
Project Scope: predict whether a customer will delay his/her credit card bill payment
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

def encode_features(X):
    non_numeric_columns = [item for item in list(X.columns) if item not in list(X._get_numeric_data().columns)]
    for item in non_numeric_columns:
        X[item][pd.isnull(X[item])] = "NaN"
        encoder = LabelEncoder()
        encoder.fit(X[item])
        # Transform and replace the training data
        training_encoded = encoder.transform(X[item])
        X[item] = training_encoded
    return X 
    
def split_training_data(X,y,randomState):
    datas = pd.concat([X,y["TARGET"]],axis=1)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=randomState)
    for train_index, test_index in split.split(datas,datas["TARGET"]):
        X_train = datas.loc[train_index]
        X_valid = datas.loc[test_index]
    y_train = X_train.TARGET
    y_test = X_valid.TARGET
    X_train = X_train.drop(["TARGET"],axis=1)
    X_test = X_valid.drop(["TARGET"],axis=1)
    
    return X_train,X_test,y_train,y_test
  
def preprocessing(X_train,X_valid=None,y_train=None,y_valid=None):
    sc = StandardScaler()
    lda = LDA(n_components=1)

    #Replace NA values with mean of column to compute dimensionality reduction
    X_train = X_train.fillna(X_train.mean())
    X_valid = X_valid.fillna(X_valid.mean())
    #scalarization for multi layer perceptron
    X_train = sc.fit_transform(X_train)
    X_valid = sc.transform(X_valid)
    #dimensionality reduction
    X_train = pd.DataFrame(lda.fit_transform(X_train,y_train))
    X_valid = pd.DataFrame(lda.transform(X_valid))

    return X_train,X_valid,y_train,y_valid
    
def RandomForest(X_train,X_test,y_train):
    classifier = RandomForestClassifier(max_depth=5, random_state=0)#
    classifier.fit(X_train, y_train)
    preds1 = classifier.predict_proba(X_test)
    preds1 = preds1[:,1]
#    auc_scr = roc_auc_score(y_valid, preds1)
#    print("AUC Score: {}".format(auc_scr))
    return preds1

def GradientBoosting(X_train,X_test,y_train):
    classifier = GradientBoostingClassifier()
    classifier.fit(X_train, y_train)
    preds2 = classifier.predict_proba(X_test)
    preds2 = preds2[:,1]
#    auc_scr = roc_auc_score(y_valid, preds2)
#    print("AUC Score: {}".format(auc_scr))
    return preds2
    
def MultilayerPerceptron(X_train,X_valid,y_train):
    classifier = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)
    classifier.fit(X_train, y_train)
    preds3 = classifier.predict_proba(X_test)
    preds3 = preds3[:,1]
#    auc_scr = roc_auc_score(y_valid, preds3)
#    print("AUC Score: {}".format(auc_scr))
    return preds3
 
    
if __name__ == "__main__":
   
    file_path1 = "C:/Users/celal.yanpar/OneDrive - Dogus Planet Elektronik Ticaret ve Bilisim Hizmetleri A.S/Desktop/final_project/training_data.csv"
    file_path2 = "C:/Users/celal.yanpar/OneDrive - Dogus Planet Elektronik Ticaret ve Bilisim Hizmetleri A.S/Desktop/final_project/training_label.csv"
    
    X = pd.read_csv(file_path1)
    y = pd.read_csv(file_path2)
    
    X = encode_features(X)
    
    X_train,X_test,y_train,y_test = split_training_data(X,y,345)
    X_train,X_test,y_train,y_test = preprocessing(X_train,X_test,y_train,y_test)
    
    
    mlp = pd.DataFrame(MultilayerPerceptron(X_train,X_test,y_train))
    gb = pd.DataFrame(GradientBoosting(X_train,X_test,y_train))
    rf =pd.DataFrame(RandomForest(X_train,X_test,y_train))
    predictions = pd.concat([rf,gb,mlp],axis=1)
    
    final_pred = predictions.mean(axis=1)
    overall_auc_scr = roc_auc_score(y_test, final_pred)
    
    print("AUC Score: {}".format(overall_auc_scr))
