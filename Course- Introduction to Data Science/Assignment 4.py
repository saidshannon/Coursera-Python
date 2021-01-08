import pandas as pd
import timeit
import numpy as np
import re
import scipy.stats as stats

#CIties dataframe replacing blank values with Nan and then dropping the Nan values
cities=pd.read_html('datasets/wikipedia_data.html')[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
cities=cities.rename(columns={'Population (2016 est.)[8]':'Population'})
for i in cities['NHL']:
    for j in i:
        if j=='[':
            x = re.findall('\w+(?=\[)', i)
            if(len(x)==0):
                x=[""]
            cities['NHL']=cities['NHL'].replace(i,x[0])
cities['NHL']=cities['NHL'].replace(['','—'],np.nan)
cities=cities.dropna(subset=["NHL"])


cities=cities.reset_index()
#print(cities[['Metropolitan area','NHL','Population']])

#NHL dataframe cropping other years
nhl_df=pd.read_csv('datasets/nhl.csv')
nhl_df=nhl_df.set_index('year').drop([2014,2015,2017],axis=0)

#Dropping the division names
z=list()
for i in nhl_df['team']:
    if i[-1]=='*':
        nhl_df['team']=nhl_df['team'].replace(i,i[:-1])
    y=re.match('\w+\sDivision',i)
    if y:
        z.append(i)
nhl_df=nhl_df.set_index('team').drop(z,axis=0)
nhl_df.reset_index(inplace=True)


#Making a column of win ratio and arranging according to metropolitan area
nhl_df[['W','L']]=nhl_df[['W','L']].astype(float)
nhl_df['W/L']=nhl_df['W']/(nhl_df['W']+nhl_df['L'])
nhl_df=nhl_df.sort_values(by='team',ascending=True).reset_index()
cities=cities.sort_values(by='Metropolitan area',ascending=True).reset_index()
#print(nhl_df[['team','W/L']])
#print(cities[['Metropolitan area','NHL','Population']])

#Creating a list Z of the teams whose average we have to take and a list P of all the 31 teams
Z=list()
P=list()
for i in cities['NHL']:
    X=re.match('\w+\s',i)
    if X:
        P.append(i)
        continue
    else:
        Y=re.findall('[A-Z][a-z]+',i)
    if len(Y)>1:
        Z.append(Y)

        continue
    P.append(i)
#print(Z)
for i in Z:
    for j in i:
        P.append(j)

#Creating a list of all team names to rename the team column
G=list()
for i in nhl_df['team']:
    for j in P:
        if j in i:
            G.append(j)
nhl_df['team']=G
df=nhl_df[['team','W/L']]
df.set_index('team',inplace=True)

#FInding average of the teams in same area
N=list()
L=list()
for i in Z[0]:
    for k in df.loc[i]:
        N.append(k)
N=np.average(N)
#print(N)
for j in Z[1]:
    for k in df.loc[j]:
        L.append(k)
L=np.average(L)
#print(L)

#Adding the teams to the column and dropping the teams whose average was taken
df=df.drop(Z[0],axis=0)
df=df.drop(Z[1],axis=0)
name=str()
name1=str()
for i in Z[0]:
    name=name+i
for i in Z[1]:
    name1=name1+i
df.loc[name]=N
df.loc[name1]=L


df=df.reset_index()
cities=cities.rename(columns={'NHL':'team'})
#Merging the dataframes finally with corresponding team names
DF=pd.merge(df,cities[['Metropolitan area','team']],how='right',on='team')
population_by_region = list(cities['Population'].astype(float)) # pass in metropolitan area population from cities
win_loss_by_region = list(DF['W/L'])# pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

print(stats.pearsonr(population_by_region,win_loss_by_region))
print(population_by_region)
print(win_loss_by_region)
W=[0.4142857142857143, 0.7142857142857143, 0.35714285714285715, 0.5138888888888888, 0.5070422535211268, 0.4583333333333333, 0.589041095890411, 0.6, 0.5675675675675675, 0.43478260869565216, 0.47368421052631576, 0.5945945945945946, 0.6338028169014085, 0.42028985507246375, 0.7464788732394366, 0.39436619718309857, 0.6176470588235294, 0.618421052631579, 0.625, 0.5789473684210527, 0.7012987012987013, 0.6533333333333333, 0.43661971830985913, 0.68, 0.6533333333333333, 0.7222222222222222, 0.622894633764199, 0.5182014205986808]
P=[4794447.0, 1132804.0, 1392609.0, 9512999.0, 2041520.0, 7233323.0, 2853077.0, 4297617.0, 1321426.0, 2155664.0, 13310447.0, 6066387.0, 3551036.0, 4098927.0, 1865298.0, 20153634.0, 1323783.0, 6070500.0, 4661537.0, 2342299.0, 1302946.0, 6657982.0, 2807002.0, 3032171.0, 5928040.0, 2463431.0, 6131977.0, 778489.0]
