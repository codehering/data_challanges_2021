# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:58:24 2021
This script creates the different label variables for kmeans, dbscan and hierarchical cluster analysis. This is necessary for filtering differnt clustering methods in shiny dashboard. 
@author: annalena, freddy
"""

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
directory = "timeperiod/old/"
old_files = ["data_400bc_labels.csv", "data_200bc_labels.csv", "data_0bc_labels.csv", "data_0ad_labels.csv", "data_200ad_labels.csv"]
data_files = ["data_400bc.csv", "data_200bc.csv", "data_0bc.csv", "data_0ad.csv", "data_200ad.csv"]
feature = ['weight', 'enddate', 'startdate', 'material_cat', 'denom_cat',
       'mint_cat']
output = list()

# rename old label variable and execute dbscan clustering
for old_file_name in old_files:
    data = pd.read_csv(f"{directory+old_file_name}", sep=";")
    data = data.rename(columns={"label": "kmeans_label"})
    # do dbscan analysis
    tmp = data[["x", "y"]]
    dbscan = DBSCAN(eps=2, min_samples=1).fit(tmp)
    data["dbscan_label"] = dbscan.labels_
    output.append(data)

# load full dataset for hierarchical clustering (doesnt work with umap results)
data = pd.read_csv('data\\analysis_dataset_w_material.csv', sep=";")

#helper method for plotting dendrograms for hierarchical cluster analysis
def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)



for c in data.columns:
    try:
        data[c] = data[c].astype(float)
    except:
        print(c)
del data["findspot"]
del data["material"]
data = data[feature]

# create data subsets
full_datasets = [data[data["enddate"] <= -400], data[(data["enddate"]>-400) & (data["enddate"]<=-200)], data[(data["enddate"]>-200) & (data["enddate"]<=0)], data[(data["enddate"]>0) & (data["enddate"]<=200)], data[data["enddate"]>200]]
full_datasets = [x.dropna() for x in full_datasets]
counter = 1
#first analyze agglomerative cluster resutls and set threshold for number of clusters
for dataset in full_datasets:
    model = AgglomerativeClustering(n_clusters=None, affinity='euclidean', distance_threshold=0,)
    model = model.fit(dataset)
    plt.title(f"{counter}")
    counter +=1
    plot_dendrogram(model)
    plt.show()
#1: 11
#2: 15
#3: 26
#4: 12
#5: 16
counter = 0
# n_cluster threshold from analysis above.
clusters = [11, 15, 26, 12, 16]
for dataset in full_datasets:
    model = AgglomerativeClustering(n_clusters=clusters[counter], affinity='euclidean').fit(dataset)
    output[counter]["hierarchy_label"] = model.labels_
    counter +=1
i = 0
# export datasets
for out in output:
    out.to_csv(f"timeperiod/{old_files[i]}", sep=";", index=False)
    i += 1

