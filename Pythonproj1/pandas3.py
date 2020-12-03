import pandas as pd
import re

df=pd.read_csv("datasets/presidents.csv")
#print(df.head())
df["First"]=df["President"].apply(lambda x:x.split()[0])
df['Last']=df["President"].apply(lambda x:x.split()[-1])
#print(df[["First","Last"]])

df1=pd.read_csv("datasets/log.csv")
#print(df1.head())
#print(" ")
#print(df1.isnull().head())
#df1.fillna(0,inplace=True)
#print(df1.head())
df1=df1.set_index(['time','user'])
df1=df1.sort_index()
#print(df1.head(20))
#print(" ")
df1.fillna(method='ffill',inplace=True)
#print(df1.head(20))


df2=pd.read_csv('datasets/Admission_Predict.csv',index_col=0)
#print(df2.head())
#print(" ")
#print(df2.columns)
df2.rename(mapper=str.strip,axis=1,inplace=True)
#print(df2[df2["Chance of Admit"]>0.7])
print(df2['Chance of Admit'].gt(0.7) & df2['Chance of Admit'].lt(0.9))
#print(df2[df2['Chance of Admit'].gt(0.7) & df2['Chance of Admit'].lt(0.9)].head())

