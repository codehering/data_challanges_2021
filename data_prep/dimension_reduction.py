# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 19:40:03 2021

@author: fredi
"""

import pandas as pd
import numpy as np
import umap.umap_ as umap
import umap.utils
import umap.plot
import json
import requests
import random
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
def prepare_data(data):
    data["weight"] = [float(str(x).replace(",",".")) for x in data["weight"]]
    data["mint"] = [x.replace("http://nomisma.org/id/", "") for x in data["mint"]]
    data["coin"] = [x.split("#coins?id=")[1] for x in data["coin"]]
    data["material"] = [x.replace("http://nomisma.org/id/", "") for x in data["material"]]
    data["denom"] = [x.replace("http://nomisma.org/id/", "") for x in data["denom"]]
    data["findspot"] = [str(x).replace("file:///C:/Users/karsten/Documents/uni/ProgrammeWorkspace/D2RServer/d2rq-0.8.1_CNT/dump_2021_03_16.rdf#", "") \
                        for x in data["findsport"]]
    data["authority"] = [x.replace(" http://nomisma.org/id/", "") for x in data["authority"]]
    categorial_vars = ["material", "denom", "mint", "collection", "weightstand_engl", "findsport", "authority", "peculiarities_engl" ]
    
    for var in categorial_vars:
        data[var] = data[var].astype('category')
        
    try:
        data['weight'] = pd.to_numeric(data['weight'],errors='coerce')
        try:
            data['maxdiam'] = pd.to_numeric(data['maxdiam'],errors='coerce')
            try: 
                data['mindiam'] = pd.to_numeric(data['mindiam'],errors='coerce')
                try:
                    data['weight'].astype(float)
                except:
                    pass
            except:
                pass
        except:
            pass
    except:
        pass
        
    return data
data = pd.read_csv("C:\\Users\\fredi\\Desktop\\Uni\\Data Challanges\\CN\\data\\queryResults_semikolon.csv", sep=";")
prepared_data = prepare_data(data)
preselection = ["coin", "weight", "startdate", "enddate", "denom", "mint", "material"]
selected_data = prepared_data[preselection]

# get geo cordinates
selected_data["mint"] = [x.replace(" ", "") for x in selected_data["mint"]]
mints = selected_data["mint"].unique().tolist()



mint_list = list()
for mint in mints:
    r = requests.get(f"http://nomisma.org/apis/getMints?id={mint}")
    text = r.text
    
    try:
        data_mint = json.loads(text)
        data_mint = data_mint["features"][0]["geometry"]["coordinates"]
        mint_list.append({"mint": mint, "lon": data_mint[0], "lat": data_mint[1]})
    except:
        print(mint)
# no geocoords for:
#eleutherion
#olbia_city
mint_geo = pd.DataFrame(mint_list)
selected_data = pd.merge(selected_data, mint_geo, how="left", on="mint")
#weighting of the material variables:
#bronze: ae
#silber: ar
#Elektron (Mangensiumligierung): el
#Gold: av
#Kupfer: cu
#Blei: pb
#Hierarchie:
# av > ar > cu > ae > el > pb
# 6 > 5 > 4 > 3 > 2 > 1
selected_data["material"] = [x.replace(" ", "") for x in selected_data["material"]]
selected_data["material"] = np.where(selected_data["material"]=="av", 6, np.where(selected_data["material"]=="ar", 5, np.where(selected_data["material"]=="cu",4, np.where(selected_data["material"]=="ae", 3, np.where(selected_data["material"]=="el", 2, np.where(selected_data["material"]=="pb", 1, np.nan))))) )
selected_data = selected_data[["coin", "weight", "startdate", "enddate", "lon", "lat", "material"]]
selected_data = selected_data.dropna()


#split up the datasets:
data_dict = dict()
data_dict["data_400bc"] = selected_data[selected_data["enddate"] <= -400]
data_dict["data_200bc"] = selected_data[(selected_data["enddate"]>-400) & (selected_data["enddate"]<=-200)]
data_dict["data_0bc"] = selected_data[(selected_data["enddate"]>-200) & (selected_data["enddate"]<=0)]
data_dict["data_0ad"] = selected_data[(selected_data["enddate"]>0) & (selected_data["enddate"]<=200)]
data_dict["data_200ad"] = selected_data[selected_data["enddate"]>200]
for key in data_dict.keys():
    print(data_dict[key].shape)

coin_dict = dict()
for key in data_dict.keys():
    coin_dict[key] = data_dict[key]["coin"].to_list()
    del data_dict[key]["coin"]

# now do umap:

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

umap_results = dict()
for key in data_dict.keys():
    print(key)
    tmp_data = StandardScaler().fit_transform(data_dict[key])
    x, y = cross_validation(tmp_data, 20)
    plt.scatter(x,y)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(f"{key}")
    plt.show()
    umap_results[key] = pd.DataFrame({"x": x, "y": y})

for key in umap_results.keys():
    umap_results[key]["coin"] = coin_dict[key]
for key in umap_results.keys():
    umap_results[key].to_csv(f"../timeperiod/new/{key}.csv", index=False)
for key in data_dict.keys():
    data_dict[key].to_csv(f"../timeperiod/new/raw/{key}.csv", index=False)
