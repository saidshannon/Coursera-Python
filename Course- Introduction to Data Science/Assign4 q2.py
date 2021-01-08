import numpy as np
import pandas as pd
import re

nba_df=pd.read_csv("datasets/nba.csv")
cities=pd.read_html("datasets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#Cleaning the team names and dropping the other years

for i in nba_df['team']:
    a=re.findall('(\w+\s*\w+\s*\w*)',i)
    nba_df['team']=nba_df['team'].replace(i,a[0])
nba_df=nba_df.set_index('year').drop([2014,2015,2016,2017],axis=0).reset_index()

#cleaning the NBA teams in cities dataframes and renaming the Population column
for i in cities['NBA']:
    if i.startswith('['):
        cities=cities.set_index('NBA').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            cities['NBA']=cities['NBA'].replace(i,b[0])
            continue
cities=cities.set_index('NBA').drop('—',axis=0).reset_index()
cities=cities.rename(columns={'Population (2016 est.)[8]':'Population'})
#print(cities[['NBA','Population']])
#print(nba_df[['team','W/L%']])

#Making the list of the 30 teams and the list of the teams of whose average we want
teams=list()
ateams=list()
for i in cities['NBA']:
    b=re.match('[A-Z][a-z]+[A-Z][a-z]+',i)
    if b:
        c=re.findall('[A-Z][a-z]+',i)
        ateams.append(c)
        for j in c:
            teams.append(j)
        continue
    teams.append(i)
#print(teams)
#Replacing the teams in nba dataframe without the place included
for i in nba_df['team']:
    for j in teams:
        if j in i:
            nba_df['team']=nba_df['team'].replace(i,j)

#Finding the average of the teams in the nba dataframe which our in the same region
nba_df.set_index('team',inplace=True)
nba_df['W/L%']=nba_df['W/L%'].astype(float)
d=list()
av1=np.average(nba_df['W/L%'].loc[ateams[0]].values)
av2=np.average(nba_df['W/L%'].loc[ateams[1]].values)

#Concantinating the teams whose average we found to match the ones on the city dataframe and dropping those teams from the nba teams
team1=str()
team2=str()
for i in ateams[0]:
    team1=team1+i
for j in ateams[1]:
    team2=team2+j
for i in ateams[0]:
    nba_df=nba_df.drop(i,axis=0)
for i in ateams[1]:
    nba_df=nba_df.drop(i,axis=0)

#adding the concatinated teams and their averages to the nba dataframe
nba_df.loc[team1]=av1
nba_df.loc[team2]=av2

#Merging the two dataframes cities and nba_df to get a dtaframe wiht the teams,population and the win/loss ratio
nba_df.reset_index(inplace=True)
cities.rename(columns={'NBA':'team'},inplace=True)
df=pd.merge(cities[['team','Population']],nba_df[['team','W/L%']],how='left',on='team')



population_by_region = list(df['Population']) # pass in metropolitan area population from cities
win_loss_by_region = list(df['W/L%']) # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

print(population_by_region)
print(win_loss_by_region)











