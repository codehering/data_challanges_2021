# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:36:14 2021
The aim of this script was tu understand AutoViz library, which is a usefull library for plotting and creating descriptive statistics.
@author: fredi
"""
import pandas as pd
from autoviz.AutoViz_Class import AutoViz_Class
import numpy as np
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
AV = AutoViz_Class()

data = pd.read_csv('data\\analysis_dataset.csv', sep=";")
data["denom_cat"] = data["denom_cat"].astype("category")
data["mint_cat"] = data["mint_cat"].astype("category")
data["collection_cat"] = data["collection_cat"].astype("category")
del data["Unnamed: 0"]
del data["coin"]
data.to_csv("data\\autoviz_prepared_data.csv")

df = AV.AutoViz('data\\autoviz_prepared_data.csv')


test = data.copy()
test.dropna(inplace=True)
del test["findspot"]
test.info()
for col in test.columns:
    test[col] = test[col].astype(int)

mat_cols = [x for x in test.columns.tolist() if "material" in x]
test["material"] = 0
i = 1
for c in mat_cols:
    test["material"] = np.where(test[c]==1, i, test["material"])
    i +=1
test = test[["maxdiam", "mindiam", "weight", "enddate", "startdate", "mint_cat", "denom_cat", "collection_cat", "material"]]

from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
chi_square_value,p_value=calculate_bartlett_sphericity(test)
chi_square_value, p_value
from factor_analyzer.factor_analyzer import calculate_kmo
kmo_all,kmo_model=calculate_kmo(test)
kmo_model # kmo > 0.6 -> Factor analysis can be done

fa = FactorAnalyzer()
fa.set_params(n_factors=9, rotation=None)
fa.fit(test)
ev, v = fa.get_eigenvalues()
ev
plt.scatter(range(1,10), ev)
plt.plot(range(1,10), ev)
plt.xlabel = "Factors"
plt.ylabel ="Eigenvalue"
plt.show
fa2 = FactorAnalyzer()
fa2.set_params(n_factors=4, rotation="varimax")
fa2.fit(test)
ev2, v2 = fa2.get_eigenvalues();ev2

loadings = fa2.loadings_
factors_col = list()
for f in range(1,5):
    factors_col.append(f"Factor_{f}")
factors = pd.DataFrame(fa2.loadings_, columns=factors_col, index=test.columns)

variance = pd.DataFrame(fa2.get_factor_variance(), columns=factors_col, index=["SS Loadings", "Proportion Var", "Cumulative Var"])