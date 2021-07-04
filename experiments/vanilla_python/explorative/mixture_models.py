# -*- coding: utf-8 -*-
"""
Created on Sun May 23 15:45:25 2021
The aim of this script was to understand Gaussian and Bayesian mixture models (GME/BME) for clustering.
With this script we were able to get a feel for GME/BME and we came to the conclusion that GME/BME offers no added value as a cluster algorithm compared to kmeans or dbscan.
For this reason, GME/BME was not used for the analysis part. 
@author: freddy, annalena
"""

import pandas as pd
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
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


imp = IterativeImputer(max_iter=10, random_state=0)
imp_data = data.copy()
head = data.columns
for col in data.columns:
    imp.fit(np.array(data[col]).reshape(-1,1))
    imp_data[col] = imp.transform(np.array(data[col]).reshape(-1,1))
    

# Set up a range of cluster numbers to try
n_range = range(2,11)

# Create empty lists to store the BIC and AIC values
bic_score = []
aic_score = []
X = imp_data.copy()
# Loop through the range and fit a model
for n in n_range:
    gm = GaussianMixture(n_components=n, 
                         random_state=123, 
                         n_init=10)
    gm.fit(X)
    
    # Append the BIC and AIC to the respective lists
    bic_score.append(gm.bic(X))
    aic_score.append(gm.aic(X))
    
# Plot the BIC and AIC values together
fig, ax = plt.subplots(figsize=(12,8),nrows=1)
ax.plot(n_range, bic_score, '-o', color='orange')
ax.plot(n_range, aic_score, '-o', color='green')
ax.set(xlabel='Number of Clusters', ylabel='Score')
ax.set_xticks(n_range)
ax.set_title('BIC and AIC Scores Per Number Of Clusters')

model = GaussianMixture(n_components=2)
model.fit(X)
yhat = model.predict(X)
clusters = set(yhat)
from numpy import where
for cluster in clusters:
	# get row indexes for samples with this cluster
	row_ix = where(yhat == cluster)
	# create scatter of these samples
	plt.scatter(X[row_ix, 0], X[row_ix, 1])
# show the plot
plt.show()

pca = PCA(n_components=2)
pca.fit(X)
X_pca = pca.transform(X)



bgm = BayesianGaussianMixture(n_components=6, n_init=10)
bgm.fit(X_pca)
test = bgm.predict(X_pca)
df_pca = pd.DataFrame(X_pca, columns=["PCA1", "PCA2"])
df_pca["labels"] = test
data["labels"] = test
plt.scatter(df_pca.PCA1, df_pca.PCA2, c=df_pca.labels, alpha = 0.6)
plt.show()
for i in range(6):
    tmp = data[data["labels"]==i]
    plt.scatter(tmp.maxdiam, tmp.weight, c=tmp.labels, alpha = 0.6)
    plt.show()
np.round(bgm.weights_, 2)
