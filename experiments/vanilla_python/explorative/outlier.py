# -*- coding: utf-8 -*-
"""
Created on Sun May 23 17:05:26 2021
This script was created to test an outlier detection algorithm. However, we could not gather any useful insights and the use of outlier detection was not pursued in the further project process.
@author: fredi
"""

from sklearn.ensemble import IsolationForest
import pandas as pd
from sklearn.impute import IterativeImputer
import numpy as np

data = pd.read_csv("data\\analysis_dataset.csv", sep=";")
del data["Unnamed: 0"]
coins = data["coin"].to_list()
del data["coin"]
del data["axis"]
del data["mindiam"]
del data["findspot"]
imp = IterativeImputer(max_iter=10, random_state=0)
imp_data = data.copy()
head = data.columns
for col in data.columns:
    imp.fit(np.array(data[col]).reshape(-1,1))
    imp_data[col] = imp.transform(np.array(data[col]).reshape(-1,1))
    #to do single transformation
#imp_data = imp.transform(data)
imp_data = pd.DataFrame(imp_data, columns=head)


# use isolation forest for detecting outlier
clf = IsolationForest()
preds = clf.fit_predict(imp_data)
imp_data["outlier"] = preds

imp_outlier = imp_data[imp_data["outlier"]==-1]
imp_normal = imp_data[imp_data["outlier"]!=-1]
