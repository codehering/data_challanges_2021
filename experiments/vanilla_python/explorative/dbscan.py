# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:23:45 2021
The aim of this script was to understand dbscan clustering algorithm.
@author: annalena, freddy
"""

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.experimental import enable_iterative_imputer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
data = pd.read_csv("data\\analysis_dataset.csv", sep=";")
del data["Unnamed: 0"]
coins = data["coin"].to_list()
del data["coin"]
del data["axis"]
del data["mindiam"]
del data["findspot"]

for col in data.columns:
    data[col] = [str(x).replace(",",".") for x in data[col]]
    data[col] = data[col].astype(float)
imp = IterativeImputer(max_iter=10, random_state=0)
#imp.fit(data)


imp_data = data.copy()
head = data.columns
for col in data.columns:
    imp.fit(np.array(data[col]).reshape(-1,1))
    imp_data[col] = imp.transform(np.array(data[col]).reshape(-1,1))
    #to do single transformation
#imp_data = imp.transform(data)
normalize_cols = ["maxdiam", "weight", "enddate", "startdate"]
imp_data = pd.DataFrame(imp_data, columns=head)

#pca start
pca = PCA(n_components=5)
pca.fit(imp_data)
X_pca = pca.transform(imp_data)


pca_data.explained_variance_ratio_

imp_data_numerical = imp_data[normalize_cols]
imp_data = imp_data.drop(normalize_cols, axis=1)
scale = StandardScaler()
imp_data_numerical = scale.fit_transform(imp_data_numerical)
imp_data_numerical = pd.DataFrame(data=imp_data_numerical, columns=normalize_cols)
imp_data = imp_data.join(imp_data_numerical, how='outer')

imp_data_numerical.corr()
imp_data_sample = imp_data[["maxdiam", "startdate"]]
clustering = DBSCAN(eps=3, min_samples=10).fit(X_pca)

labels = clustering.labels_
data["labels"] = labels
unique_sampels = set(labels.tolist())
data_notnan = data[data["labels"]!=-1]
imp_data["labels"] = labels
data_nans = imp_data[imp_data["labels"]==-1]
# another round of clustering:
del data_nans["labels"]
pca = PCA(n_components=5)
pca.fit(data_nans)
X_pca_nans = pca.transform(data_nans)
clustering = DBSCAN(eps=5, min_samples=10).fit(X_pca_nans)
labels = clustering.labels_
unique_sampels_2 = set(labels.tolist())

plt.scatter(data_notnan.maxdiam, data_notnan.weight, c=data_notnan.labels, alpha = 0.6)
plt.show()






samples = dict()
for label in labels:
    tmp = data[data["labels"]==label]
    samples[label] = tmp.describe()