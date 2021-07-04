# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:23:57 2021
This script helped us to understand hierarchical clustering (with complete dataset).
@author: annalena, freddy
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc

data = pd.read_csv('data\\analysis_dataset_w_material.csv', sep=";")
#del data["mindiam"]
del data["axis"]
del data["Unnamed: 0"]
del data["findspot"]
del data["material"]

data = data.dropna()
data.shape

# create dendrogram for analysis
plt.figure(figsize=(10, 7))
plt.title("Customer Dendograms")
dend = shc.dendrogram(shc.linkage(data, method='ward'))