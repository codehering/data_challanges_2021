# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 12:47:07 2021

@author: freddy, annalena
"""

import rdflib
import time
import json
start_time = time.time()
graph = rdflib.Graph()
graph.open("store", create=True)
graph.parse("dump_2021_03_16.rdf")


result_dict = dict()
count = 0

# get all triples in graph, this step takes a few minutes
for subject, predicate, obj in graph:
    subject = str(subject)
    predicate = str(predicate)
    obj = str(obj)
    if subject in result_dict.keys():
        if predicate in result_dict[subject].keys():
            result_dict[subject][predicate].append(obj)
        else:
            result_dict[subject][predicate] = [obj]
    else:
        result_dict[subject] = dict()
        result_dict[subject][predicate] = [obj]
# create a dict containing every coin
keys = list(result_dict.keys())
coins = list()
for k in keys:
    k_split = k.split("/dump_2021_03_16.rdf#coins?id=")
    if len(k_split)>1:
        coins.append(k)

final_results = dict()
result = result_dict.copy()
for coin in coins:
    final_results[coin] = dict()
    coin_dict = result_dict[coin]
    for coin_dict_key in coin_dict.keys():
        for element in coin_dict[coin_dict_key]:
            if element in result_dict.keys():
                if not element in coins:
                    final_results[coin][element] = result_dict[element]
            else:
                final_results[coin][coin_dict_key] = coin_dict[coin_dict_key]
print("--- %s seconds ---" % (time.time() - start_time))              
# read big data

#search for additional metada for every coin
start_time = time.time()
additional_keys = list()
dic = final_results.copy()
counter = 0
out_dict = dict()
for key in dic.keys():
    sub_dic = dic[key]
    for sub_key in sub_dic.keys():
        if isinstance(sub_dic[sub_key], dict):
            for n_key in sub_dic[sub_key].keys():
                for e in sub_dic[sub_key][n_key]:
                    if e in result_dict.keys():
                        additional_keys.append(e)
        if isinstance(sub_dic[sub_key], list):
            for element in sub_dic[sub_key]:
                if element in result_dict.keys():
                    additional_keys.append(element)
    for new_keys in additional_keys:
        sub_dic[new_keys] = result_dict[new_keys]
    out_dict[key] = sub_dic
    counter +=1
    additional_keys = list()
    print(counter)
#save the data
with open(f'data/cn_output.json', "w") as file:
    json.dump(out_dict, file)
print("--- %s seconds ---" % (time.time() - start_time))
