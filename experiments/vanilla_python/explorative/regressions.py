# -*- coding: utf-8 -*-
"""
Created on Sun May 30 16:32:22 2021
this script was created to  get a better understanding oif the relationship between individual features and their realtions with logistic regression models. 
@author: freddy, annalena
"""
import pandas as pd
import statsmodels.api as sm


data = pd.read_csv('data\\analysis_dataset.csv', sep=";")
data = data.dropna()

del data["Unnamed: 0"]
del data["coin"]
del data["axis"]
del data["mindiam"]
del data["findspot"]
del data["enddate"]
y = data["startdate"]
X = data.drop("startdate", axis=1)
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()
est.summary() # r^2 0.616

weight = data["weight"]
weight = sm.add_constant(weight)
simple1 = sm.OLS(y, weight).fit()
simple1.summary() #r^2 0.15
maxdiam = data["maxdiam"]
maxdiam = sm.add_constant(maxdiam)
simple2 = sm.OLS(y, maxdiam).fit()
simple2.summary() #r^2 0.33

weightdiam = data[["weight", "maxdiam"]]
weightdiam = sm.add_constant(weightdiam)
simple3 = sm.OLS(y, weightdiam).fit()
simple3.summary() #r^2 0.41

import statsmodels.formula.api as smf
weightdiam["y"] = y
simple4 = smf.ols(formula="y ~ weight*maxdiam", data=weightdiam).fit()
simple4.summary() #r^2 0.42

#logit
data_not_dummy = data[["weight", "maxdiam", "startdate", "denom_cat", "mint_cat", "collection_cat"]]
y = data["material_ ae "]
X = data_not_dummy
X = sm.add_constant(X)
logit1 = sm.Logit(y, X).fit()
logit1.summary() #r^2 0.68

y = data["material_ ar "]
X = data_not_dummy
X = sm.add_constant(X)
logit2 = sm.Logit(y, X).fit()
logit2.summary() #r^2 0.71

y = data["material_ av "]
X = data_not_dummy
X = sm.add_constant(X)
logit3 = sm.Logit(y, X).fit()
logit3.summary() #r^2: 0.32

y = data["material_ cu "]
X = data_not_dummy
X = sm.add_constant(X)
logit4 = sm.Logit(y, X).fit()
logit4.summary() #r^2 : 0.21
#always maxdiam un denom_cat not significant

# el and pb have not enought observations
y = data["material_ el "]
X = data_not_dummy
X = sm.add_constant(X)
logit5 = sm.Logit(y, X).fit()
logit5.summary() #Perfect separation detected

y = data["material_ pb "]
X = data_not_dummy
X = sm.add_constant(X)
logit6 = sm.Logit(y, X).fit()
logit6.summary() # perfect separation detected
