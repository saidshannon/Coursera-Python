import  pandas as pd
import numpy as np
import re
#Remove rows of header and skip footers
energy=pd.read_excel('datasets/Energy Indicators.xls',skiprows=16,skipfooter=38)
Q=energy
#dropping not needed columns
x=energy.columns
energy=energy.drop([x[0],x[1]],axis=1)

#removing the string values in the column Energy Supply and replacing the blank values with nan
energy['Energy Supply']=energy['Energy Supply'].transform(lambda x:np.nan if type(x)==str else x )
energy=energy.replace('',np.nan)

#renaming the columns and changing petajoules to gigajoules
energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy['Energy Supply']=energy['Energy Supply'].transform(lambda x:x*1000000)



#removing parentheses in countries
pattern="(\w*)\s\("
energy=energy.dropna(subset=['Country'])



#removing the added number in the end of some countries
for i in energy['Country']:
    for j in i:
        if(j=='('):
            z = re.findall(pattern, i)
            energy['Country']=energy['Country'].replace(i,z[0])
        for k in range(30):
            if(j==str(k)):
                X=i[:-1]
                energy['Country']=energy['Country'].replace(i,X)
                i=X

#renaming the list of countries
countries={"Republic of Korea": "South Korea","United States of America": "United States","United Kingdom of Great Britain and Northern Ireland": "United Kingdom","China, Hong Kong Special Administrative Region": "Hong Kong"}
for i,j in countries.items():
    energy['Country']=energy['Country'].replace(i,j)


#Skipping the header of the next dataframe and renaming the countries and renaming the Column Country name
GDP=pd.read_csv('datasets/world_bank.csv',skiprows=4)
Countries={"Korea, Rep.": "South Korea","Iran, Islamic Rep.": "Iran","Hong Kong SAR, China": "Hong Kong"}
GDP.rename(columns={"Country Name":"Country"},inplace=True)

for i,j in Countries.items():
    GDP['Country']=GDP['Country'].replace(i,j)

#Loading the skimagojr-3 dataframe
ScimEn=pd.read_excel('datasets/scimagojr-3.xlsx')


#Merging the dataframes
k=GDP.columns
GDP=GDP.drop(k[1:50],axis=1)
df=pd.merge(ScimEn,energy,how='left',on='Country')
df1=pd.merge(df,GDP,how='left',on='Country').set_index('Country')
#print(df1.head(15)
#df1=df1.head(15)

###########
print(len(energy))
print(len(ScimEn))
print(len(GDP))
sum=len(Q)+len(ScimEn)+len(GDP)
print(sum-len(df1))

###########################

cols=['2006', '2007', '2008','2009', '2010', '2011', '2012', '2013', '2014', '2015']
s=pd.Series(df1[cols].mean(axis=1))
s.sort_values(ascending=False,inplace=True)
#print(s.keys())

###########################

country=s.keys()

df1=df1.reset_index()
df2=df1[df1['Country']==country[5]]
x=np.abs(df2['2006']-df2['2015'])
#print(x)
#for i,j in x.items():
    #print(j)

#################
#print(df1['Energy Supply per Capita'].agg(np.nanmean))

#################

df1=df1.set_index('Country')
df3=df1['% Renewable'].sort_values(ascending=False)
#for i,j in df3.items():
    #print(tuple([i,j]))
    #break

##########################


df1['Rcitations']=df1['Self-citations']/df1['Citations']
df4=df1['Rcitations'].sort_values(ascending=False)
#print(df4)
#for i,j in df4.items():
   #print(tuple([i,j]))
    #break
###########################

a=df1['Energy Supply']/df1['Energy Supply per Capita']
#print(a)
b=a.sort_values(ascending=False)
#print(b)
c=list()
for i,j in b.items():
    c.append(i)
#print(c[2])

############################

df1['Pop']=df1['Energy Supply']/df1['Energy Supply per Capita']
df1['C']=df1['Citable documents']/df1['Pop']
#print(df1[['Energy Supply per Capita','Citable documents']])
df5=df1[['C','Energy Supply per Capita']].astype(float)
#print(df5.dtypes)
#print(df5['C'].corr(df5['Energy Supply per Capita']))

############################

#df1.sort_values(ascending=False,by="% Renewable",inplace=True)
m=np.median(df1['% Renewable'])
df1.reset_index(inplace=True)
df1[['Country','Rank']]=df1[['Country','Rank']].sort_values(by='Rank',ascending=True)
df1.set_index("Country",inplace=True)
df1['Mean']=df1['% Renewable'].transform(lambda x: 1 if x>=m else 0)
#print(df1['Mean'])

###########################

ContinentDict  = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America'}
u=list()
v=list()
for i,j in ContinentDict.items():
    u.append(i)
    v.append(j)
DF=pd.DataFrame({'Country':u,'Continent':v})
DF['size']=DF.groupby('Continent').transform(lambda x:len(x))
DF=pd.merge(DF,df1['Pop'],how='left',on="Country")
DF=DF.set_index('Continent').drop_duplicates()
DF['sum']=DF.groupby('Continent')['Pop'].transform(np.sum)
DF['Pop']=DF['Pop'].astype(float)
DF['mean']=DF.groupby('Continent')['Pop'].transform(np.average)
DF['std']=DF.groupby('Continent')['Pop'].transform(lambda x: x.std())
DF=DF.drop(['Pop','Country'],axis=1)
DF=DF.drop_duplicates()
DF.reset_index(inplace=True)
DF=DF.sort_values(by='Continent')
DF=DF.set_index('Continent')
#print(DF)

###################################
df.set_index('Country',inplace=True)
A=pd.cut(df1["% Renewable"],5)
A=A.sort_values(ascending=False)
df6=pd.DataFrame({'Country':u,'Continent':v})
df6=df6.merge(A,how='right',on='Country')
df6=df6.set_index(['Continent','% Renewable']).groupby(['Continent','% Renewable']).apply(lambda x:len(x))
#print(df6)

###################################
#e.g. 12345678.90 -> 12,345,678.90
df1.reset_index(inplace=True)
df1['Pop']=df1['Pop'].astype(str)
v=list()
for i in df1['Pop']:
    i=i.split('.')
    z=i[0]
    sum=0
    count=0
    j=str()
    for k in z[::-1]:
        sum=sum+1
        count=count+1
        if (count==len(z)):
            j = j + k
            break
        if (sum == 3):
            j=j+k+','
            sum=0
            continue
        j=j+k
    y=str()
    for l in j[::-1]:
        y=y+l
    y=y+'.'+i[1]
    v.append(y)
t=list()
for i in df1['Country']:
    t.append(i)
df7=pd.Series(v,index=t)
#print(df7)


















