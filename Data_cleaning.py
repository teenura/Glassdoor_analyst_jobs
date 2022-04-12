# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 12:45:48 2022

@author: Teenura
"""

import pandas as pd
df=pd.read_csv("D:\JOBS_DATA\Glassdoor_scrapped_data.csv")

#Find out if salary is employer provided or glassdoor estimate and total missing salary
df['Employer_provided']=df['Salary'].apply(lambda x: 1 if 'employer provided' in x.lower() else 0)
df['Glassdoor_estimate']=df['Salary'].apply(lambda x: 1 if 'glassdoor estimate' in x.lower() else 0)
missing_salary=len(df[df['Salary']=='-1'])

#parse salary data to get lower nd upper salary limit
salary_clean=df['Salary'].apply(lambda x: x.replace('\u20B9 ','').replace('L','').replace(' ','').replace('(EmployerProvided)','').\
                                replace('(GlassdoorEstimate)',''))
df['Upper_salary']=salary_clean.apply(lambda x: float(x.split('-')[1]) if x!='-1' else float(-1))
df['Lower_salary']=salary_clean.apply(lambda x: float(x.split('-')[0]) if x!='-1' else float(-1))
df['Avg']=(df['Upper_salary']+df['Lower_salary'])/2

#Age of company
df['Age']=df['Founded'].apply(lambda x: x if x<0 else 2022-x) 

#Cleaning Size, Revenue
df['Size']=df['Size'].apply(lambda x: x.replace('Unknown','-1'))
df['Revenue']=df['Revenue'].apply(lambda x: x.replace('Unknown / Non-Applicable','-1'))

#Remove all rows with all of salary, location, size, revenue null
df=df[(df['Location']!='-1') | (df['Size']!='-1') | (df['Revenue']!='-1')]
all_null=df[(df['Location']=='-1') & (df['Size']=='-1') & (df['Revenue']=='-1') & (df['Salary']=='-1')]

#Cleaning location
location_count=df['Location'].value_counts()
df['Location']=df['Location'].apply(lambda x: x.replace('Bangalore','Bengaluru').replace('Secunderabad','Hyderabad').replace('Delhi','Delhi NCR').replace('New Delhi','Delhi NCR').replace('Gurgaon','Delhi NCR').replace('Noida','Delhi NCR').replace('Navi Mumbai','Mumbai'))
df['Location']=df['Location'].apply(lambda x: x.replace('Delhi NCR NCR','Delhi NCR'))
location_count_1=df['Location'].value_counts()   

#Parse description for skills required
df['Job Description']=df['Job Description'].astype(str)
df['Python_yn']=df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() or ' r ' in x.lower() or '.r ' in x.lower() else 0)
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
excel_count=df.excel.value_counts()
df['SQL']=df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
sql_count=df['SQL'].value_counts()
df['ML']=df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() or ' ml ' in x.lower() or 'learning' in x.lower() else 0)
df['NLP']=df['Job Description'].apply(lambda x: 1 if 'natural language' in x.lower() else 0)
df['Visualisation']=df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() or 'powerbi' in x.lower() or 'power bi' in x.lower() or 'visualisation' in x.lower() else 0)
df['ML'].value_counts()

#Impute missing values using average upper and lower salary over Location, Revenue, Size
num_size=df['Size'].value_counts()
num_revenue=df['Revenue'].value_counts()

#Compute average upper and lower salary over Location, Revenue, Size
df_notnull=df[(df['Location']!='-1') & (df['Size']!='-1') & (df['Revenue']!='-1') & (df['Salary']!='-1')]
avg_3=df_notnull.groupby(['Location','Size','Revenue']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})
avg_lr=df_notnull.groupby(['Location','Revenue']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})
avg_ls=df_notnull.groupby(['Location','Size']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})
avg_rs=df_notnull.groupby(['Size','Revenue']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})
avg_l=df_notnull.groupby(['Location']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})
avg_r=df_notnull.groupby(['Revenue']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})
avg_s=df_notnull.groupby(['Size']).agg({'Upper_salary':'mean' , 'Lower_salary':'mean'})

i_list=avg_3.index.tolist()
df_copy=df
   
no_null=df[(df['Location']!='-1') & (df['Size']!='-1') & (df['Revenue']!='-1')]    
no_null_c=no_null.groupby(['Location','Size','Revenue']).count() 
len(avg_3)-len(no_null_c) #3 multi_indexes dont have any non null data and hence cannot be utilised for filling missing data

df=df.astype({'Upper_salary':'str','Lower_salary':'str'})       
    
def rep_upsal(x,a,b,c,d,e,f,g):
    m=x['Location']
    n=x['Size']
    o=x['Revenue']
    if m!='-1' and n!='-1' and o!='-1':
        if (m,n,o) in a.index.tolist():
            return str(a.loc[(m,n,o),'Upper_salary'])
        else:
            return '-1.0'
    elif m!='-1' and n=='-1' and o!='-1':
        return str(b.loc[(m,o),'Upper_salary'])
    elif m!='-1' and n!='-1' and o=='-1':
        return str(c.loc[(m,n),'Upper_salary'])
    elif m=='-1' and n!='-1' and o!='-1':
        return str(d.loc[(n,o),'Upper_salary'])
    elif m!='-1' and n=='-1' and o=='-1':
        return str(e.loc[m,'Upper_salary'])
    elif m=='-1' and n=='-1' and o!='-1':
        return str(f.loc[o,'Upper_salary'])
    elif m=='-1' and n!='-1' and o=='-1':
        return str(g.loc[n,'Upper_salary'])

def rep_lowsal(x,a,b,c,d,e,f,g):
    m=x['Location']
    n=x['Size']
    o=x['Revenue']
    tup=(m,n,o)
    if m!='-1' and n!='-1' and o!='-1':
        if tup in a.index.tolist():
            return str(a.loc[(m,n,o),'Lower_salary'])
        else:
            return '-1.0'
    elif m!='-1' and n=='-1' and o!='-1':
        return str(b.loc[(m,o),'Lower_salary'])
    elif m!='-1' and n!='-1' and o=='-1':
        return str(c.loc[(m,n),'Lower_salary'])
    elif m=='-1' and n!='-1' and o!='-1':
        return str(d.loc[(n,o),'Lower_salary'])
    elif m!='-1' and n=='-1' and o=='-1':
        return str(e.loc[m,'Lower_salary'])
    elif m=='-1' and n=='-1' and o!='-1':
        return str(f.loc[o,'Lower_salary'])
    elif m=='-1' and n!='-1' and o=='-1':
        return str(g.loc[n,'Lower_salary'])
    
d1=df
d1['Upper_salary']=d1.apply(lambda x: x['Upper_salary'].replace('-1.0',rep_upsal(x,avg_3,avg_lr,avg_ls,avg_rs,avg_l,avg_r,avg_s)) if (x['Upper_salary']=='-1.0') else x['Upper_salary'] , axis=1)
d1['Lower_salary']=d1.apply(lambda x: x['Lower_salary'].replace('-1.0',rep_lowsal(x,avg_3,avg_lr,avg_ls,avg_rs,avg_l,avg_r,avg_s)) if (x['Lower_salary']=='-1.0') else x['Lower_salary'] , axis=1)    

d1=d1.astype({'Upper_salary':'float','Lower_salary':'float'})  
d1['Avg']=(d1['Upper_salary']+d1['Lower_salary'])/2
d1=d1[d1['Avg']!=-1]

d1_salnull=d1[d1['Avg']==-1.0][['Location','Size','Revenue','Upper_salary','Lower_salary']]
d1_salnull=d1_salnull.sort_values(by=['Location','Size','Revenue'])

#Parse Job_tile to form categories of job as well as seniority
def title_simplifier(title):
    if 'data scien' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'

def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'

d1['seniority'] = d1['Job Title'].apply(seniority)
d1.seniority.value_counts()

d1['job_simp'] = d1['Job Title'].apply(title_simplifier)
d1['job_simp'].value_counts()

df_model = d1[['job_simp','seniority','Avg','Upper_salary','Lower_salary','Employer_provided','Glassdoor_estimate','Location','Rating','Size','Type of ownership','Industry','Sector','Revenue','Age','Python_yn','R_yn','spark','aws','excel','SQL','ML','NLP','Visualisation']]


df_model.to_csv('Glassdoor_data_cleaned.csv')

















