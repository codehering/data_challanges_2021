# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 14:49:06 2021
this script was used to investigate different dimension reduction algorithms apart from UMAP. In particular, t-SNE and truncated SVD were used and explicitly investigated with the entity data. 
@author: annalena, freddy
"""
import pandas as pd
from sklearn.manifold import TSNE    
import time
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import TruncatedSVD
import random
import umap.umap_ as umap
import umap.utils
import umap.plot


cat_dummys = pd.read_csv("2021_06_01_DC_NLP_CNT\\entity_cats_prepared.csv", sep=";")
del cat_dummys["Unnamed: 0"]

#split categorys by side
cat_dummys_obv = cat_dummys[cat_dummys["side"]==0]
cat_dummys_rev = cat_dummys[cat_dummys["side"]==1]
cat_dummys_sides = pd.merge(cat_dummys_obv, cat_dummys_rev, how="outer", on="id_coin")
cat_coins = cat_dummys_sides["id_coin"]
del cat_dummys_sides["id_coin"]
cat_dummys_sides = cat_dummys_sides.fillna(-1)

#try t-SNE algorithm
time_start = time.time()
tsne = TSNE(n_components=2, verbose=2, perplexity=40, n_iter=1000, learning_rate=10)
tsne_results = tsne.fit_transform(cat_dummys_sides)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))
plt.scatter(
    tsne_results[:, 0],
    tsne_results[:, 1])
plt.gca().set_aspect('equal', 'datalim')


#try good old umap
def cross_validation(d, k=40):
    seeds = random.sample(range(0, 100000), k)
    embedding_x = 0
    embedding_y = 0
    counter = 0
    for seed in seeds:
        counter += 1
        print(f"{counter}/{k}")
        r = umap.UMAP(random_state=seed)
        r.fit(d)
        embedding = r.transform(d)
        embedding_x += embedding[:, 0]
        embedding_y += embedding[:, 1]
    embedding_x = embedding_x / k
    embedding_y = embedding_y / k
    return embedding_x, embedding_y
x, y = cross_validation(cat_dummys_sides, 10)
plt.scatter(
    x,
    y)
umap_cat_df = pd.DataFrame({"x": x, "y": y})

# use umap to cluster data
clustering = DBSCAN(eps=1, min_samples=10).fit(umap_cat_df)
umap_cat_df["label"] = clustering.labels_
plt.scatter(
    umap_cat_df["x"],
    umap_cat_df["y"], c= umap_cat_df["label"])
umap_cat_df.groupby("label").count()


# use SVD for sparse daata
svd = TruncatedSVD(n_components=2, n_iter=100, random_state=42)
svd.fit(cat_dummys_sides)
svd_data = svd.transform(cat_dummys_sides)
plt.scatter(
    svd_data[:, 0],
    svd_data[:, 1])

d_tmp = pd.read_csv("2021_06_01_DC_NLP_CNT\\design_data2.csv", sep=";")
e_tmp = pd.read_csv("2021_06_01_DC_NLP_CNT\\entity_cats.csv", sep=";")

complete_data = pd.merge(d_tmp, e_tmp, how="left", left_on="Entity", right_on="name")

cat_cols = [x for x in complete_data if "Cat" in x]
complete_data = complete_data[["id_coin"]+cat_cols]
data_list = list()
for cluster in svd_df["label"].unique().tolist():
    tmp = svd_df[svd_df["label"]==cluster]
    tmp_coins = tmp["coin"].unique().tolist()
    tmp_cats = complete_data[complete_data["id_coin"].isin(tmp_coins)]
    tmp_dict = dict()
    for c in cat_cols:
        tmp_dict[c] = tmp_cats[c].unique().tolist()
        tmp_dict[c] = [x for x in tmp_dict[c] if str(x) != "nan"]
    data_list.append(tmp_dict)

test = data_list[0]
catI_list =list()
for d in data_list:
    catI_list.append(d["Cat_I"])