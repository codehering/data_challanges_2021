# -*- coding: utf-8 -*-
"""
Created on Wed May 26 21:31:32 2021
This script helped us to understand and get a feeling with kmeans clustering. We also experimented with an imputer and PCA. 
@author: annalena, freddy
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv("data\\analysis_dataset.csv", sep=";")

del data["Unnamed: 0"]
del data["coin"]
del data["axis"]
del data["mindiam"]
del data["findspot"]


# impute values
imp = IterativeImputer(max_iter=10, random_state=0)
imp_data = data.copy()
head = data.columns
for col in data.columns:
    imp.fit(np.array(data[col]).reshape(-1,1))
    imp_data[col] = imp.transform(np.array(data[col]).reshape(-1,1))


# split up intervals for better analysis:
interval_costs = list()
intervals = [range(1,16), range(15,101) , range(100,200), range(200,300), range(300, 400)]
k_ = range(15,100)
for i in intervals:
    costs = list()
    for k in i:
        print(k)
        kmeans = KMeans(n_clusters=k, random_state=0).fit(imp_data)
        costs.append(kmeans.inertia_)
    interval_costs.append(costs)

for j in range(len(interval_costs)):
    plt.plot(intervals[j], interval_costs[j])
    plt.show()
plt.plot(k_, costs)

kmeans = KMeans(n_clusters=500, random_state=0).fit(imp_data)
imp_data["labels"] = kmeans.labels_

# PCA
X_pca = pd.DataFrame(X_pca, columns=["PCA1", "PCA2"])
X_pca["labels"] = kmeans.labels_
plt.scatter(X_pca.PCA1, X_pca.PCA2, c=X.labels, alpha = 0.6)
plt.show()
test = imp_data.groupby("labels")["maxdiam"].count()
