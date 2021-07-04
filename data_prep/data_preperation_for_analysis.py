# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:23:45 2021
This script loads the results from the sparql query and prepares them for further analysis. 
@author: annalena, freddy
"""

import pandas as pd
import numpy as np
data = pd.read_csv("data\\queryResults_semikolon.csv", sep=";")

#filter for interesting variables
filter_vars = ["coin",  "maxdiam", "mindiam", "weight", "material", "enddate", "startdate", "denom", "mint", "collection", "weightstand_engl", "findsport", "authority", "peculiarities_engl", "axis"]

data = data[filter_vars]


# replace unnecessary prefixes
data["mint"] = [x.replace("http://nomisma.org/id/", "") for x in data["mint"]]
data["coin"] = [x.split("#coins?id=")[1] for x in data["coin"]]
data["material"] = [x.replace("http://nomisma.org/id/", "") for x in data["material"]]
data["denom"] = [x.replace("http://nomisma.org/id/", "") for x in data["denom"]]
data["findspot"] = [str(x).replace("file:///C:/Users/karsten/Documents/uni/ProgrammeWorkspace/D2RServer/d2rq-0.8.1_CNT/dump_2021_03_16.rdf#", "") for x in data["findsport"]]
categorial_vars = ["material", "denom", "mint", "collection", "weightstand_engl", "findsport", "authority", "peculiarities_engl" ]

# create nan values for further filtering
for var in categorial_vars:
    data[var] = data[var].replace("  ", np.nan)

fill_ratio = 100 - data.isnull().sum(axis = 0)/len(data)*100

#delete findsport, authority, pecularities_engl and weightstand_engl because fill ratio is less than 15%
del data["findsport"]
categorial_vars.remove("findsport")
del data["authority"]
categorial_vars.remove("authority")
del data["peculiarities_engl"]
categorial_vars.remove("peculiarities_engl")
del data["weightstand_engl"]
categorial_vars.remove("weightstand_engl")

#check number of different observations

for var in categorial_vars:
    print(f"{var} : {len(data[var].unique().tolist())}")

#only for material its possible to create dummy variables:
print(data["material"].value_counts())
material_dummys = pd.get_dummies(data["material"], prefix="material")
data = data.join(material_dummys)
categorial_vars.remove("material")
del data["material"]
# cat encoding for denom, mint and collection
for var in categorial_vars:
    data[var] = data[var].astype('category')
    data[f"{var}_cat"] = data[var].cat.codes
#delete collection, mint and denom. Lot of missing values hard to inteprete.
del data["collection"]
del data["mint"]
del data["denom"]
#fix , . problem for float values
for col in data.columns:
    data[col] = [str(x).replace(",",".") for x in data[col]]
    try:
        data[col] = data[col].astype(float)
    except:
        pass
# create dataset for algorithms:
dataset = data.copy()



# export dataset
dataset.to_csv("data\\analysis_dataset.csv", sep=";")
