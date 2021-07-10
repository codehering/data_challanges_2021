# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:58:24 2021

@author: fredi
"""

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
directory = "../timeperiod/new/"
data_files = ["data_400bc.csv", "data_200bc.csv", "data_0bc.csv", "data_0ad.csv", "data_200ad.csv"]

# elbow analysis for kmeans clustering
for file in data_files:
    tmp_data = pd.read_csv(f"{directory+file}")
    tmp_data = tmp_data[["x", "y"]]
    Sum_of_squared_distances = list()
    K = range(1,20)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(tmp_data)
        Sum_of_squared_distances.append(km.inertia_)
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title(f'{file} - Elbow Method For Optimal k')
    plt.show()

# optimal k values
k_values = [4,4, 4, 4, 5]
i = 0
k_labels = list()
for file in data_files:
    tmp_data = pd.read_csv(f"{directory+file}")
    tmp_data = tmp_data[["x", "y"]]
    km = KMeans(n_clusters=k_values[i])
    i += 1
    km = km.fit(tmp_data)
    k_labels.append(km.labels_)

#dbscan clustering analysis
dbscan_labels = list()
for file in data_files:
    # do dbscan analysis
    tmp_data = pd.read_csv(f"{directory+file}")
    tmp_data = tmp_data[["x", "y"]]
    dbscan = DBSCAN(eps=2, min_samples=1).fit(tmp_data)
    dbscan_labels.append(dbscan.labels_)




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



#first analyze agglomerative cluster resutls and set threshold for number of clusters
for file in data_files:
    tmp_data = pd.read_csv(f"../timeperiod/new/raw/{file}")
    model = AgglomerativeClustering(n_clusters=None, affinity='euclidean', distance_threshold=0,)
    model = model.fit(tmp_data)
    plt.title(f"{file}")
    plot_dendrogram(model)
    plt.show()
#1: 11
#2: 15
#3: 26
#4: 12
#5: 16
counter = 0
#optimal number of classes for hierarchical clustering
clusters = [8, 8, 6, 3, 6]
hierarchy_labels = list()
for file in data_files:
    tmp_data = pd.read_csv(f"../timeperiod/new/raw/{file}")
    model = AgglomerativeClustering(n_clusters=clusters[counter], affinity='euclidean').fit(tmp_data)
    hierarchy_labels.append(model.labels_)
    counter +=1
c = 0
# output
for file in data_files:
    data = pd.read_csv(f"{directory+file}")
    data["kmeans_label"] = k_labels[c]
    data["dbscan_label"] = dbscan_labels[c]
    data["hierarchy_label"] = hierarchy_labels[c]
    data.to_csv(f"../timeperiod/new/{file.replace('.csv','')}_labels.csv", index=False)
    
    
    c +=1


