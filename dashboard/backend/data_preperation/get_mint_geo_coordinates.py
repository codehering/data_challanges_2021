# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 21:14:19 2021
This scripts sources geo coordinates for a given mint. We planned to integrate a geo map analysis. However, we decided to use a simple bar chart for visualizing mint distribution. 
@author: freddy, annalena
"""
import requests
import json
import pandas as pd

data = pd.read_csv("../data/full_cnn_dataset.csv" , sep=";")
mints = set(data["mint"].to_list())
mints = [x.replace(" ", "") for x in mints if x != ""]



outlist = list()
for mint in mints:
# use nomisma api request
    r = requests.get(f"http://nomisma.org/apis/getMints?id={mint}")
    text = r.text
    data = json.loads(text)
    try:
        data= data["features"][0]["geometry"]["coordinates"]
        outlist.append({"mint": mint, "lon": data[0], "lat": data[1]})
    except:
        print(mint)
    
# olbia_city, eleutherion do not have valid geo coodrinates
df = pd.DataFrame(outlist)
df.to_csv("mint_geo.csv")
