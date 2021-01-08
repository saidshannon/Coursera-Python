import pandas as pd
import numpy as np
import re
import scipy.stats as stats

mlb_df=pd.read_csv("datasets/mlb.csv")
nhl_df=pd.read_csv("datasets/nhl.csv")
nba_df=pd.read_csv("datasets/nba.csv")
nfl_df=pd.read_csv("datasets/nfl.csv")
cities=pd.read_html("datasets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
c1=cities
c2=cities
c3=cities
c4=cities
c5=cities
c6=cities


#NHL excel cleaning
nhl_df=nhl_df.set_index('year').drop([2014,2015,2017],axis=0).reset_index()
z=list()
for i in nhl_df['team']:
    if i[-1]=='*':
        nhl_df['team']=nhl_df['team'].replace(i,i[:-1])
    y=re.match('\w+\sDivision',i)
    if y:
        z.append(i)
nhl_df=nhl_df.set_index('team').drop(z,axis=0)
nhl_df.reset_index(inplace=True)
nhl_df[['W','L']]=nhl_df[['W','L']].astype(float)
nhl_df['W/L']=nhl_df['W']/(nhl_df['W']+nhl_df['L'])
nhl_df.set_index('team',inplace=True)
#print(nhl_df['W/L'])


#NBA excel cleaning
for i in nba_df['team']:
    a=re.findall('(\w+\s*\w+\s*\w*)',i)
    nba_df['team']=nba_df['team'].replace(i,a[0])
nba_df=nba_df.set_index('year').drop([2014,2015,2016,2017],axis=0).reset_index()
nba_df.set_index('team',inplace=True)
nba_df['W/L%']=nba_df['W/L%'].astype(float)
#print(nba_df['W/L%'])

#NFL excel cleaning
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
nfl_df['W-L%']=nfl_df['W-L%'].astype(float)
nfl_df.set_index('team',inplace=True)
#print(nfl_df['W-L%'])

#MLB excel cleaning
mlb_df=mlb_df.set_index('year').drop([2014,2015,2016,2017],axis=0).reset_index()
mlb_df.set_index('team',inplace=True)
#print(mlb_df['W-L%'])

#########First Pair(NBA-NHL)
#NBA column cleaning
for i in c1['NBA']:
    if i.startswith('['):
        c1=c1.set_index('NBA').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            c1['NBA']=c1['NBA'].replace(i,b[0])
            continue
c1=c1.set_index('NBA').drop('—',axis=0).reset_index()
c1=c1.rename(columns={'Population (2016 est.)[8]':'Population'})


#NHL column cleaning
for i in c1['NHL']:
    for j in i:
        if j=='[':
            x = re.findall('\w+(?=\[)', i)
            if(len(x)==0):
                x=[""]
            c1['NHL']=c1['NHL'].replace(i,x[0])
c1['NHL']=c1['NHL'].replace(['','—'],np.nan)
c1=c1.dropna(subset=["NHL"])
c1=c1.reset_index()
#print(c1[['Metropolitan area','NHL','NBA']])


#Making the list of a list of teams in each area
x=list()
y=list()
for i,j in zip(c1['NHL'],c1['NBA']):
    a=re.findall('\w+\s\w+|[A-Z][a-z]+',i)
    b=re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+',j)
    x.append(a)
    y.append(b)

#Appending all the average values of all the teams in NHL
nhl=list()
av=list()
average=0
#print(x)
#print(y)
#print(nhl_df['W/L'])
for i in x:
    for l in i:
        for j,k in nhl_df['W/L'].items():
            if l in j:
                av.append(k)
    average=np.average(av)
    nhl.append(average)
    average=0
    av=[]

#Appending all the average values of all the teams in NBA
nba=list()
av1=list()
average1=0
for i in y:
    for j in i:
        for k,l in nba_df['W/L%'].items():
            if j in k:
                av1.append(l)
    average1=np.average(av1)
    nba.append(average1)
    average1=0
    av1=[]

#print(len(nhl))
#print(len(nba))
A=stats.ttest_rel(nhl,nba)
#print(A)

###########Second Pair(NBA-NFL)
#NBA column cleaning
for i in c2['NBA']:
    if i.startswith('['):
        c2=c2.set_index('NBA').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            c2['NBA']=c2['NBA'].replace(i,b[0])
            continue
c2=c2.set_index('NBA').drop('—',axis=0).reset_index()
c2=c2.rename(columns={'Population (2016 est.)[8]':'Population'})

#NFL column cleaning
for i in c2['NFL']:
    if i.startswith('['):
        c2=c2.set_index('NFL').drop(i,axis=0).reset_index()
    a=re.match('\w+\[',i)
    if a:
        b=re.findall('\w+(?=\[)',i)
        c2['NFL']=c2['NFL'].replace(i,b[0])
    if i.startswith('— '):
        c2=c2.set_index('NFL').drop(i,axis=0).reset_index()

c2=c2.set_index('NFL').drop('—',axis=0).reset_index()

#print(c2[['Metropolitan area','NFL','NBA']])

#
x=list()
y=list()
for i,j in zip(c2['NBA'],c2['NFL']):
    a = re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+', i)
    b = re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+', j)
    x.append(a)
    y.append(b)

#print(len(x))
#print(len(y))

#
nba=list()
av=list()
average=0
for i in x:
    for j in i:
        for k,l in nba_df['W/L%'].items():
            if j in k:
                av.append(l)
    average=np.average(av)
    nba.append(average)
    av=[]
    average=0
#print(len(nba))

#NFL
nfl=list()
av=list()
average=0
for i in y:
    for j in i:
        for k,l in nfl_df['W-L%'].items():
            if j in k:
                av.append(l)
    average=np.average(av)
    nfl.append(average)
    av=[]
    average=0
#print(len(nfl))

B=stats.ttest_rel(nba,nfl)
#print(B)

###Third Pair (NBA-MLB)

#MLB column cleaning
for i in c3['MLB']:
    if i.startswith('['):
        c3=c3.set_index('MLB').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            c3['MLB']=c3['MLB'].replace(i,b[0])
            continue
c3=c3.set_index('MLB').drop('—',axis=0).reset_index()
c3=c3.rename(columns={'Population (2016 est.)[8]':'Population'})

#NBA column cleaning
for i in c3['NBA']:
    if i.startswith('['):
        c3=c3.set_index('NBA').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            c3['NBA']=c3['NBA'].replace(i,b[0])
            continue
c3=c3.set_index('NBA').drop('—',axis=0).reset_index()
c3=c3.rename(columns={'Population (2016 est.)[8]':'Population'})

#print(c3[['Metropolitan area','NBA',"MLB"]])

x=list()
y=list()
for i,j in zip(c3['NBA'],c3['MLB']):
    a = re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+', i)
    b = re.findall('[A-Z][a-z]+\s\w+|[A-Z][a-z]+|\w+\s\w+|[0-9]+[a-z]+', j)
    x.append(a)
    y.append(b)
#print(len(x))
#print(y)
#
nba=list()
av=list()
average=0
for i in x:
    for j in i:
        for k,l in nba_df['W/L%'].items():
            if j in k:
                av.append(l)
    average=np.average(av)
    nba.append(average)
    av=[]
    average=0
#print(nba)

#
mlb=list()
av=list()
average=0
for i in y:
    for j in i:
        for k,l in mlb_df['W-L%'].items():
            if j in k:
                av.append(l)
    average=np.average(av)
    mlb.append(average)
    av=[]
    average=0
#print(mlb)
C=stats.ttest_rel(nba,mlb)
#print(C)

#####Fourth Pair (NHL,NFL)

#
for i in c4['NFL']:
    if i.startswith('['):
        c4=c4.set_index('NFL').drop(i,axis=0).reset_index()
    a=re.match('\w+\[',i)
    if a:
        b=re.findall('\w+(?=\[)',i)
        c4['NFL']=c4['NFL'].replace(i,b[0])
    if i.startswith('— '):
        c4=c4.set_index('NFL').drop(i,axis=0).reset_index()

c4=c4.set_index('NFL').drop('—',axis=0).reset_index()

#
for i in c4['NHL']:
    for j in i:
        if j=='[':
            x = re.findall('\w+(?=\[)', i)
            if(len(x)==0):
                x=[""]
            c4['NHL']=c4['NHL'].replace(i,x[0])
c4['NHL']=c4['NHL'].replace(['','—'],np.nan)
c4=c4.dropna(subset=["NHL"])
c4=c4.reset_index()
#print(c1[['Metropolitan area','NHL','NBA']])


#
x=list()
y=list()
for i,j in zip(c4['NHL'],c4['NFL']):
    a = re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+', i)
    b = re.findall('[A-Z][a-z]+\s\w+|[A-Z][a-z]+|\w+\s\w+|[0-9]+[a-z]+', j)
    x.append(a)
    y.append(b)

#
nhl=list()
av=list()
average=0
#print(x)
#print(y)
#print(nhl_df['W/L'])
for i in x:
    for l in i:
        for j,k in nhl_df['W/L'].items():
            if l in j:
                av.append(k)
    average=np.average(av)
    nhl.append(average)
    average=0
    av=[]

#
nfl=list()
av=list()
average=0
for i in y:
    for j in i:
        for k,l in nfl_df['W-L%'].items():
            if j in k:
                av.append(l)

    average=np.average(av)
    nfl.append(average)
    av=[]
    average=0
D=stats.ttest_rel(nfl,nhl)
#print(D)

####Fifth Pair(NHL,MLB)

#
for i in c5['NHL']:
    for j in i:
        if j=='[':
            x = re.findall('\w+(?=\[)', i)
            if(len(x)==0):
                x=[""]
            c5['NHL']=c5['NHL'].replace(i,x[0])
c5['NHL']=c5['NHL'].replace(['','—'],np.nan)
c5=c5.dropna(subset=["NHL"])
c5=c5.reset_index()
#print(c1[['Metropolitan area','NHL','NBA']])

#
for i in c5['MLB']:
    if i.startswith('['):
        c5=c5.set_index('MLB').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            c5['MLB']=c5['MLB'].replace(i,b[0])
            continue
c5=c5.set_index('MLB').drop('—',axis=0).reset_index()
c5=c5.rename(columns={'Population (2016 est.)[8]':'Population'})

#
x=list()
y=list()
for i,j in zip(c5['NHL'],c5['MLB']):
    a = re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+', i)
    b = re.findall('[A-Z][a-z]+\s\w+|[A-Z][a-z]+|\w+\s\w+|[0-9]+[a-z]+', j)
    x.append(a)
    y.append(b)

#
nhl=list()
av=list()
average=0
for i in x:
    for l in i:
        for j,k in nhl_df['W/L'].items():
            if l in j:
                av.append(k)
    average=np.average(av)
    nhl.append(average)
    average=0
    av=[]

#
mlb=list()
av=list()
average=0
for i in y:
    for j in i:
        for k,l in mlb_df['W-L%'].items():
            if j in k:
                av.append(l)
    average=np.average(av)
    mlb.append(average)
    av=[]
    average=0

E=stats.ttest_rel(nhl,mlb)
#print(E)

########Sixth Pair(NFL,MLB)

#
for i in c6['NFL']:
    if i.startswith('['):
        c6=c6.set_index('NFL').drop(i,axis=0).reset_index()
    a=re.match('\w+\[',i)
    if a:
        b=re.findall('\w+(?=\[)',i)
        c6['NFL']=c6['NFL'].replace(i,b[0])
    if i.startswith('— '):
        c6=c6.set_index('NFL').drop(i,axis=0).reset_index()
c6=c6.set_index('NFL').drop('—',axis=0).reset_index()

#
for i in c6['MLB']:
    if i.startswith('['):
        c6=c6.set_index('MLB').drop(i,axis=0).reset_index()
        continue
    for j in i:
        if j=='[':
            b=re.findall('\w+\s*\w*(?=\[)',i)
            c6['MLB']=c6['MLB'].replace(i,b[0])
            continue
c6=c6.set_index('MLB').drop('—',axis=0).reset_index()
c6=c6.rename(columns={'Population (2016 est.)[8]':'Population'})

#print(c6[['Metropolitan area','NFL','MLB']])

#
x=list()
y=list()
for i,j in zip(c6['NFL'],c6['MLB']):
    a = re.findall('\w+\s\w+|[0-9]+[a-z]+|[A-Z][a-z]+', i)
    b = re.findall('[A-Z][a-z]+\s\w+|[A-Z][a-z]+|\w+\s\w+|[0-9]+[a-z]+', j)
    x.append(a)
    y.append(b)

#
nfl=list()
av=list()
average=0
for i in x:
    for j in i:
        for k,l in nfl_df['W-L%'].items():
            if j in k:
                av.append(l)

    average=np.average(av)
    nfl.append(average)
    av=[]
    average=0


#
mlb=list()
av=list()
average=0
for i in y:
    for j in i:
        for k,l in mlb_df['W-L%'].items():
            if j in k:
                av.append(l)

    average=np.average(av)
    mlb.append(average)
    av=[]
    average=0

F=stats.ttest_rel(nfl,mlb)
#print(F)
#[NBA.NHL,NFL,MLB]
sports = ['NFL', 'NBA', 'NHL', 'MLB']
p_values=pd.DataFrame({k: np.nan for k in sports},index=sports)
pvalue=[B,D,F,A,C,E]
pvalues=list()
for i,j in pvalue:
    pvalues.append(j)
print(pvalues)
k=0
for i in sports:
    for j in sports:

        if i==j:
            continue
        for m in pvalues:
            if p_values.loc[i,j]==m:
                D=1
                break
        if D==1:
            D=0
            continue
        if k == 6:
            break
        p_values.loc[i,j]=p_values.loc[j,i]=pvalues[k]
        k=k+1

print(p_values)
print(p_values.loc["NBA", "NHL"])

