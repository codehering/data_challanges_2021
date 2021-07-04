# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:04:18 2021

@author: fredi
"""

import pandas as pd
design_data = pd.read_csv("2021_06_01_DC_NLP_CNT\\design_data2.csv", sep=";")
#delete vers
design_data = design_data[design_data["Label_Entity"]!="VERBS"]
del design_data["DesignID"]



entity_dummys = pd.get_dummies(design_data["Entity"], prefix="entity")
entity_dummys["id_coin"] = design_data["id_coin"]
cols = [x for x in entity_dummys.columns if "entity" in x]
g = entity_dummys.groupby("id_coin")[cols].sum().reset_index()

g.to_csv("design_dummys.csv", sep=";")
