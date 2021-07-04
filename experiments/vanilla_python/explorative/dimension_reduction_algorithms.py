# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 11:51:30 2021
This script was used to explore different dimension reduction algorithms like UMAP, truncated SVD, t-SNE or a neural network as autoencoder. 
@author: annalena, freddy
"""
import pandas as pd
import umap.umap_ as umap
import umap.utils
import umap.plot
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
data = pd.read_csv('data\\analysis_dataset_w_material.csv', sep=";")
del data["mindiam"]
del data["axis"]
del data["Unnamed: 0"]
data = data.dropna()
data.shape
del data["findspot"]
coins = data["coin"].to_list()
data["material"] = data["material"].astype("category")
data["material"] = data["material"].cat.codes
for c in data.columns:
    try:
        data[c] = data[c].astype(float)
    except:
        print(c)
del data["coin"]
scaled_data = StandardScaler().fit_transform(data)
scaled_data = pd.DataFrame(scaled_data)
scaled_data["coin"] = coins
design_data = pd.read_csv("2021_06_01_DC_NLP_CNT\\design_dummys.csv", sep=";")
svd = TruncatedSVD(n_components=2, n_iter=20, random_state=42)
design_coins = design_data["id_coin"].to_list()
del design_data["id_coin"]
del design_data["Unnamed: 0"]
svd.fit(design_data)
new = svd.transform(design_data)
new = pd.DataFrame(new)
new["id_coin"] = design_coins
complete_data = pd.merge(scaled_data, new, how="left", left_on="coin", right_on="id_coin")
print(complete_data.shape)
complete_data = complete_data.dropna()
coins = complete_data["coin"]
del complete_data["coin"]

del complete_data["id_coin"]
print(complete_data.shape)


from sklearn.decomposition import TruncatedSVD

#mapper = umap.UMAP(metric='cosine', random_state=42, init='random').fit(complete_data) not working due to gpu
svd = TruncatedSVD(n_components=50, n_iter=10, random_state=42)
svd.fit(complete_data)
new = svd.transform(complete_data)

import matplotlib.pyplot as plt
plt.scatter(
    new[:, 0],
    new[:, 1])
plt.gca().set_aspect('equal', 'datalim')

r2 = umap.UMAP(random_state=42)
r2.fit(new)
embedding2 = r.transform(new)

plt.scatter(
    embedding2[:, 0],
    embedding2[:, 1])
plt.gca().set_aspect('equal', 'datalim')

x2, y2 = cross_validation(new)
plt.scatter(
    x2,
    y2)
plt.gca().set_aspect('equal', 'datalim')

r = umap.UMAP(random_state=42)
r.fit(complete_data)
embedding = r.transform(complete_data)
plt.scatter(
    embedding[:, 0],
    embedding[:, 1])
plt.gca().set_aspect('equal', 'datalim')

import random
def cross_validation(d, k=40):
    seeds = random.sample(range(0, 100000), k)
    embedding_x = 0
    embedding_y = 0
    for seed in seeds:
        r = umap.UMAP(random_state=seed)
        r.fit(d)
        embedding = r.transform(d)
        embedding_x += embedding[:, 0]
        embedding_y += embedding[:, 1]
    embedding_x = embedding_x / k
    embedding_y = embedding_y / k
    return embedding_x, embedding_y

x, y = cross_validation(complete_data, k=20)

plt.scatter(
    x,
    y)
plt.gca().set_aspect('equal', 'datalim')

cluster_dataset = pd.DataFrame({"x": x, "y": y})
clustering = DBSCAN(eps=1, min_samples=10).fit(cluster_dataset)
labels = clustering.labels_
cluster_dataset["label"] = labels

plt.scatter(
    cluster_dataset["x"],
    cluster_dataset["y"], c=cluster_dataset["label"])
plt.gca().set_aspect('equal', 'datalim')

from sklearn.cluster import DBSCAN




plt.scatter(
    embedding[:, 0],
    embedding[:, 1])
plt.gca().set_aspect('equal', 'datalim')

#try autoencoder
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint

def get_autoencoder(dims, act='relu'):
    n_stacks = len(dims) - 1
    x = Input(shape=(dims[0],), name='input')

    h = x
    for i in range(n_stacks - 1):
        h = Dense(dims[i + 1], activation=act, name='encoder_%d' % i)(h)

    h = Dense(dims[-1], name='encoder_%d' % (n_stacks - 1))(h)
    for i in range(n_stacks - 1, 0, -1):
        h = Dense(dims[i], activation=act, name='decoder_%d' % i)(h)

    h = Dense(dims[0], name='decoder_0')(h)

    model = Model(inputs=x, outputs=h)
    model.summary()
    return model
X = complete_data.values
X_train, X_test = train_test_split(X, test_size=0.2, random_state=11)
batch_size = 32
pretrain_epochs = 10
encoded_dimensions = 50
shape = [X.shape[-1], 1000, 1000, 500, encoded_dimensions]
autoencoder = get_autoencoder(shape)
print(shape)

encoded_layer = f'encoder_{(len(shape) - 2)}'

print(f'taking the last encoder layer:{encoded_layer}')

hidden_encoder_layer = autoencoder.get_layer(name=encoded_layer).output
encoder = Model(inputs=autoencoder.input, outputs=hidden_encoder_layer)
autoencoder.compile(loss='mse', optimizer='adam')
#train
model_series = 'CLS_MODEL_' + datetime.now().strftime("%h%d%Y-%H%M")

checkpointer = ModelCheckpoint(filepath=f"{model_series}-model.h5", verbose=0, save_best_only=True)

autoencoder.fit(
    X_train,
    X_train,
    batch_size=batch_size,
    epochs=pretrain_epochs,
    verbose=1,
    validation_data=(X_test, X_test),
    callbacks=[checkpointer]
)

autoencoder = load_model(f"{model_series}-model.h5")

weights_name = 'weights/' + model_series + "-" + str(pretrain_epochs) + '-ae_weights.h5'
autoencoder.save_weights(weights_name)

X_encoded = encoder.predict(X)


def learn_manifold(x_data, umap_min_dist=0.00, umap_metric='euclidean', umap_dim=10, umap_neighbors=30):
    md = float(umap_min_dist)
    return umap.UMAP(
        random_state=0,
        metric=umap_metric,
        n_components=umap_dim,
        n_neighbors=umap_neighbors,
        min_dist=md).fit_transform(x_data)

X_reduced = learn_manifold(X_encoded, umap_neighbors=30, umap_dim=2)#int(encoded_dimensions/2))
plt.scatter(
    X_reduced[:, 0],
    X_reduced[:, 1])
plt.gca().set_aspect('equal', 'datalim')


#check tsne:
from sklearn.manifold import TSNE    
import time
cat_dummys = pd.read_csv("2021_06_01_DC_NLP_CNT\\entity_cats_prepared.csv", sep=";")
del cat_dummys["Unnamed: 0"]
del cat_dummys["id_coin"]
time_start = time.time()
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(cat_dummys)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))
plt.scatter(
    tsne_results[:, 0],
    tsne_results[:, 1])
plt.gca().set_aspect('equal', 'datalim')