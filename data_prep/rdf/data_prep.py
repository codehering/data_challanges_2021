# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 21:45:29 2021
The idea of this script was to directly extract the data from RDF format via python.
But we have found that it makes more sense to access the data directly via sparql. For this reason this script is no longer relevant

@author: freddy, annalena
"""

import json
import time
import pandas as pd
with open("cn_output.json", "r") as file:
    data = json.load(file)
keys = list(data.keys())[0]
test = data[keys]
coin_dict = dict()
out_dict = dict()
start_time = time.time()
data_keys = list(data.keys())#[:1000]
# flatten dictionaries
for coin in data_keys:
    coin_data = data[coin]
    for k in coin_data.keys():
        if isinstance(coin_data[k], dict):
            subdict = coin_data[k]
            for j in subdict.keys():
                print(j)
                if "#obverse" in k:
                    n = j + "#obverse"
                elif "#reverse" in k:
                    n = j + "#reverse"
                else:
                    n = j
                if not j in coin_data.keys():
                    coin_dict[n] = subdict[j]
        else:
            coin_dict[k] = coin_data[k]
    out_dict[coin] = coin_dict
    coin_dict = dict()
print("--- %s seconds ---" % (time.time() - start_time)) 
with open("cn_output_flatten.json", "w") as file:
    json.dump(out_dict, file)    
#unlist the values

with open("cn_output_flatten.json", "r") as file:
    out_dict = json.load( file)  
unlisted_outdict = dict()

def replace_prefixes(colname):
    if "http://nomisma.org/ontology" in colname:
        return colname.replace("http://nomisma.org/ontology", "nm")
    if "http://purl.org/dc/terms/" in colname:
        return colname.replace("http://purl.org/dc/terms/","purl#")
    if "http://www.w3.org/1999/02/22-rdf-syntax-ns" in colname:
        return colname.replace("http://www.w3.org/1999/02/", "w3#")
    if "http://www.w3.org/2000/01/" in colname:
        return colname.replace("http://www.w3.org/2000/01/", "w3#")
    if "http://www.w3.org/2004/02/skos/" in colname:
        return colname.replace("http://www.w3.org/2004/02/skos/", "skos#")
    if "http://xmlns.com/foaf/0.1/" in colname:
        return colname.replace("http://xmlns.com/foaf/0.1/", "#xmlns")
    print(colname)
    return colname


for key in out_dict.keys():
    coin_dict = out_dict[key]
    unlisted_coindict = dict()
    for col in coin_dict.keys():
        if len(coin_dict[col]) > 1:
            for index, value in enumerate(coin_dict[col]):
                colname = col + "_" + str(index)
                colname = replace_prefixes(colname)
                unlisted_coindict[colname] = value
        else:
            unlisted_coindict[replace_prefixes(col)] = coin_dict[col][0]
    key = key.replace("file:///C:/Users/karsten/Documents/uni/ProgrammeWorkspace/D2RServer/d2rq-0.8.1_CNT/dump_2021_03_16.rdf#coins?id=", "")
    unlisted_outdict[key] = unlisted_coindict


# dataframe format: took 2h
out_df = pd.DataFrame()
start_time = time.time()
counter = 0
for key in unlisted_outdict.keys():
    counter +=1
    df_temp = pd.DataFrame(unlisted_outdict[key], index = [0])
    df_temp["coin_dict_key"] = key
    out_df = pd.concat([out_df, df_temp], axis=0, ignore_index=True)
    print(counter)
print("--- %s seconds ---" % (time.time() - start_time))
out_df.to_csv("cn_output_df.csv", sep=";")
