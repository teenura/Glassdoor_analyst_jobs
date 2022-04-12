# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:56:22 2022

@author: Teenura
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

df = pd.read_csv('Glassdoor_data_cleaned.csv')
df.columns

df=df[(df['Size']!='-1') | (df['Revenue']!='-1') | (df['Rating']!=-1) | (df['Type of ownership']!='-1') | (df['Industry']!='-1') | (df['Sector']!='-1') | (df['Age']!=-1)]
df['Age'].value_counts()
df['Rating'].value_counts()
df4=df.replace({'-1':np.nan, -1:np.nan})

from sklearn.impute import SimpleImputer
imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
df2=imp.fit_transform(df4)
df3=pd.DataFrame(df2, columns = ['Unnamed: 0', 'job_simp', 'seniority', 'Avg', 'Upper_salary',
       'Lower_salary', 'Employer_provided', 'Glassdoor_estimate', 'Location',
       'Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
       'Age', 'Python_yn', 'R_yn', 'spark', 'aws', 'excel', 'SQL', 'ML', 'NLP',
       'Visualisation'])
df3.dtypes
df.dtypes
convert_dict = {'Avg': float,'Upper_salary': float,'Lower_salary': float,'Rating': float, 'Employer_provided':int,'Glassdoor_estimate':int,'Age':int,'Python_yn':int,'R_yn':int,'spark' :int,'aws':int,'excel':int,'SQL':int,'ML':int,'NLP':int,'Visualisation':int}
df3=df3.astype(convert_dict)
df3=df3.drop('Unnamed: 0',axis=1)

df3.to_csv('Glassdoor_nomissing_data.csv')

#linear regression
df_dum = pd.get_dummies(df3)
X = df_dum.drop(['Avg','Upper_salary','Lower_salary'], axis =1)
y = df_dum.Avg.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=34)

df1=df3.drop(['Type of ownership', 'Industry', 'Sector'], axis=1)
df1_dum = pd.get_dummies(df1)
X1=df1_dum.drop(['Avg','Upper_salary','Lower_salary'], axis =1)
y1=df1.Avg.values
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=34)

lm = LinearRegression()
lm.fit(X_train, y_train)

error1=np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

X1_sm = X1 = sm.add_constant(X1)
model1 = sm.OLS(y1,X1_sm)
model1.fit().summary()


#lasso regression
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X1_train,y1_train, scoring = 'neg_mean_absolute_error', cv= 3))

alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml,X1_train,y1_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

#Random FOrest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3))



# tune models GridsearchCV 
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# test ensembles 
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lml+tpred_rf)/2)

import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]

list(X_test.iloc[1,:])

