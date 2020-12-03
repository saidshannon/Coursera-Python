import pandas as pd
import timeit
import numpy as np
record1=pd.Series({'Name':'Alice','Subject':'Maths','Marks': 85})
record2=pd.Series({'Name':'Sam','Subject':'Maths','Marks': 85})
record3=pd.Series({'Name':'Bob','Subject':'Maths','Marks': 85})
students=[{'Name':'Alice',
           'Subject':'Maths',
            'Marks':85},
          {'Name':'Sam','Subject':'Maths','Marks': 85},
          {'Name':'Bob','Subject':'Maths','Marks': 85}]
#df1=pd.DataFrame(students,index=['student1'])
df = pd.DataFrame([record1, record2, record3],index=['student1', 'student2', 'student3'])
print(df.head())
#print(df.loc["student2",'Name'])
#print(df.loc["student1"])
#print(df['Name'])
#print(df.T.loc["Name"])
#print(df.T)
#print(df.loc['student1']['Name'])
#print(df.drop('student1'))
copy_df=df.drop('student2')
#print(copy_df.head())
df.drop('Name',inplace=True,axis='columns')
#print(df.head())
del df['Marks']
#print(df.head())
df['newcol']=None
#print(df.head())

df2=pd.read_csv('datasets/Admission_Predict.csv',index_col=0)

#print(df2.head())
new_df2=df2.rename(mapper=str.strip,axis=1)
#print(new_df2.head())
#print(new_df2.columns)
cols=list(new_df2.columns)
cols1=list()
for i in cols:
    cols1.append(i.lower())
new_df2.columns=cols1
#print(new_df2.columns)
#print(new_df2.head())
#print("Len is",len(new_df2))


#print(df3.head())
#print(len(df3))
#print(df3[df3['SUMLEV']==50])
#df3.set_index(['STNAME','CTYNAME'],inplace=True)
#print(df3.columns)
#print(df3.head())
def first_approach():
    df3 = pd.read_csv('datasets/census.csv')
    cols=df3.columns
    df3.columns=[i.lower().strip() for i in cols]
    return df3[df3["sumlev"]==50]

x=first_approach()
df3 = pd.read_csv('datasets/census.csv')
y=df3.where(df3['sumlev']==50)
#print(x)
#print(y)
def min_max(row):
    data=row[['POPESTIMATE2010',
                'POPESTIMATE2011',
                'POPESTIMATE2012',
                'POPESTIMATE2013',
                'POPESTIMATE2014',
                'POPESTIMATE2015']]
    return ("max",np.max(data),"min",np.min(data))

df3 = pd.read_csv('datasets/census.csv')
#print(df3.columns)
#print(df3['POPESTIMATE2015'])
#print(df3.apply(min_max,axis=1))

def get_state_region(x):
    northeast = ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire',
                 'Rhode Island','Vermont','New York','New Jersey','Pennsylvania']
    midwest = ['Illinois','Indiana','Michigan','Ohio','Wisconsin','Iowa',
               'Kansas','Minnesota','Missouri','Nebraska','North Dakota',
               'South Dakota']
    south = ['Delaware','Florida','Georgia','Maryland','North Carolina',
             'South Carolina','Virginia','District of Columbia','West Virginia',
             'Alabama','Kentucky','Mississippi','Tennessee','Arkansas',
             'Louisiana','Oklahoma','Texas']
    west = ['Arizona','Colorado','Idaho','Montana','Nevada','New Mexico','Utah',
            'Wyoming','Alaska','California','Hawaii','Oregon','Washington']
    if x in northeast:
        return "Northeast"
    elif x in midwest:
        return "Midwest"
    elif x in south:
        return "South"
    elif x in west:
        return "West"

#print(df3.columns)
df3['STRREG']=df3['STNAME'].apply(lambda x:get_state_region(x))

#print(df3[['STRREG','STNAME']])


