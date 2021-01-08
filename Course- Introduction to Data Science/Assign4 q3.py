import pandas as pd
import numpy as np
import re

mlb_df=pd.read_csv("datasets/mlb.csv")
cities=pd.read_html("datasets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#Cleaning the team names of the cities dataframes
for i in cities['MLB']:
    if i.startswith('['):
        cities=cities.set_index('MLB').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            cities['MLB']=cities['MLB'].replace(i,b[0])
            continue
cities=cities.set_index('MLB').drop('—',axis=0).reset_index()
cities=cities.rename(columns={'Population (2016 est.)[8]':'Population'})

#Keeping only the 2018 year data

mlb_df=mlb_df.set_index('year').drop([2014,2015,2016,2017],axis=0).reset_index()
#print(cities['MLB'])
#print(mlb_df['team'])

#Getting a list of all the teams present and the teams whose average we've to consider
teams=list()
ateams=list()
for i in cities['MLB']:
    c=re.match('[A-Z][a-z]+[A-Z][a-z]+',i)
    if c:
        d=re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+',i)
        ateams.append(d)
        for l in d:
            teams.append(l)
        continue
    teams.append(i)

#Replacing the teams in mlb dataframe with the team names from the list
for i in mlb_df['team']:
    for j in teams:
        if j in i:
            mlb_df['team']=mlb_df['team'].replace(i,j)
#print(mlb_df['team'])

#Making a list 'ateamsm' of the concantenation of those avteams to match the teams on the cities dataframe
mlb_df.set_index('team',inplace=True)
ateamsm=list()
g=str()
for i in ateams:
    for j in i:
        g=g+j
    ateamsm.append(g)
    g=''

#Getting the average of the teams whose average we have to take and adding the average to the mlb dataframe with the team name from list ateamsm
for i in range(len(ateams)):
    f=mlb_df['W-L%'].loc[ateams[i]]
    av=np.average(f.values)
    mlb_df.loc[ateamsm[i]]=av

#Dropping the teams whose average we had to take and renaming the teams in cities dataframe to teams
for i in ateams:
    mlb_df=mlb_df.drop(i,axis=0)

cities=cities.rename(columns={'MLB':'team'})

#Mergin the two dataframes with the commonn column 'teams'
mlb_df=mlb_df.reset_index()
df=pd.merge(cities[['team','Population']],mlb_df[['team','W-L%']],how='left',on='team')
print(df)


population_by_region = list(df['Population']) # pass in metropolitan area population from cities
win_loss_by_region = list(df['W-L%']) # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]
print(population_by_region,win_loss_by_region)





