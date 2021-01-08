import pandas as pd
import re
import numpy as np
import scipy.stats as stats

nfl_df=pd.read_csv("datasets/nfl.csv")
cities=pd.read_html("datasets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]


for i in cities['NFL']:
    if i.startswith('['):
        cities=cities.set_index('NFL').drop(i,axis=0).reset_index()
    a=re.match('\w+\[',i)
    if a:
        b=re.findall('\w+(?=\[)',i)
        cities['NFL']=cities['NFL'].replace(i,b[0])
    if i.startswith('— '):
        cities=cities.set_index('NFL').drop(i,axis=0).reset_index()

cities=cities.set_index('NFL').drop('—',axis=0).reset_index()


#Keeping only 2018 data and cleaning the team names
nfl_df=nfl_df.set_index('year').drop([2014,2015,2016,2017],axis=0).reset_index()
for i in nfl_df['team']:
    e = re.match('[A-Z]{3}', i)
    if e:
        nfl_df=nfl_df.set_index('team').drop(i,axis=0).reset_index()
    c=re.match('.*\+|.*\*',i)
    if c:
        b=re.findall('\w+.*(?=\*|\+)',i)
        nfl_df['team']=nfl_df['team'].replace(i,b[0])
        continue

#Creating a list of all the teams and also another list of the teams whose average we have to take
teams=list()
ateams=list()
for i in cities['NFL']:
    d=re.findall('[0-9]+[a-z]+|[A-Z][a-z]+',i)
    if len(d)>1:
        ateams.append(d)
    for j in d:
        teams.append(j)
#print(teams)
#print(ateams)

#Converting the team names in the NFL df to the ones similar to the ones in the city dataframe
for i in nfl_df['team']:
    for j in teams:
        if j in i:
            nfl_df['team']=nfl_df['team'].replace(i,j)
#print(nfl_df['team'])

#Finding the average of the teams whose average we need and adding the average to the dataframe with concatinated name
nfl_df['W-L%']=nfl_df['W-L%'].astype(float)
nfl_df.set_index('team',inplace=True)

cteam=str()
for i in ateams:
    av=np.average(nfl_df['W-L%'].loc[i].values)
    for j in i:
        cteam=cteam+j
    nfl_df.loc[cteam]=av
    cteam=''
for i in ateams:
    nfl_df=nfl_df.drop(i,axis=0)

#Renaming the population and NFl columns
nfl_df.reset_index(inplace=True)
cities=cities.rename(columns={'NFL':'team','Population (2016 est.)[8]':'Population'})
df=pd.merge(cities[['team','Population']],nfl_df[['team','W-L%']],how='left',on='team')

population_by_region = list(df['Population'].astype(float)) # pass in metropolitan area population from cities
win_loss_by_region = list(df['W-L%']) # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]
print(population_by_region)
print(win_loss_by_region)
print(stats.pearsonr(population_by_region,win_loss_by_region)[0])



