import pandas as pd
links={'GDP':'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/PY0101EN/projects/coursera_project/clean_gdp.csv',\
       'unemployment':'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/PY0101EN/projects/coursera_project/clean_unemployment.csv'}
gdp=pd.read_csv(links["GDP"])
gdp_df=pd.DataFrame(gdp)
#print(gdp_df.head())
Unemp=pd.read_csv(links["unemployment"])
Unemp_df=pd.DataFrame(Unemp)
#print(Unemp_df[Unemp_df["unemployment"]>=8.5])
x =gdp_df['date']
#print(x)
gdp_change = gdp_df['change-current']
#print(gdp_change)
unemployment=Unemp_df['unemployment']
#print(unemployment)


import pandas as pd
import timeit
import numpy as np
import re
df=pd.read_csv("datasets/listings.csv")
DF=pd.read_csv("datasets/census.csv")

record1=pd.Series({'Name':'Alice','Subject':'Maths','Marks': 85, 'A':90,'B':70})
record2=pd.Series({'Name':'Sam','Subject':'Maths','Marks': 86,'A':91, 'B':71})
record3=pd.Series({'Name':'Bob','Subject':'Arts','Marks': 87,'A':93,'B':72})
students=[{'Name':'Alice','Subject':'Maths','Marks': 85, 'A':90,'B':70},
          {'Name':'Sam','Subject':'Maths','Marks': 86,'A':91, 'B':71},
          {'Name':'Bob','Subject':'Arts','Marks': 87,'A':93,'B':72},
          {'Name':'Bob','Subject':'Maths','Marks': np.nan,'A':94,'B':73},
          {'Name':'Bob','Subject':'Arts','Marks': np.nan,'A':95,'B':74}
          ]

df1= pd.DataFrame(students,index=['student1', 'student2', 'student3','student4','student5'])
staff_df = pd.DataFrame([{'Name': 'Kelly', 'Role': 'Director of HR'},
                         {'Name': 'Sally', 'Role': 'Course liasion'},
                         {'Name': 'James', 'Role': 'Grader'}])
# And lets index these staff by name
staff_df = staff_df.set_index('Name')
# Now we'll create a student dataframe
student_df = pd.DataFrame([{'Name': 'James', 'School': 'Business'},
                           {'Name': 'Mike', 'School': 'Law'},
                           {'Name': 'Sally', 'School': 'Engineering'}])
df2=pd.DataFrame(['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D'],
                index=['excellent', 'excellent', 'excellent', 'good', 'good', 'good',
                       'ok', 'ok', 'ok', 'poor', 'poor'],
               columns=["Grades"])

#DF1=pd.merge(student_df,staff_df,how="left",left_index=True,right_index=True)
funct=lambda x:x.fillna(0.0)
g=df1.groupby('Name').aggregate(np.sqrt)
#print(df1)
g2=df1.set_index('Name').groupby('Name').apply(funct)
g1=df1.set_index('Name').groupby('Name').transform(funct)
#print(g)
#print(g2)
#print(g1)
df3=pd.DataFrame([['a', 2, 4],
                 ['a', np.nan, 3],
                ['b', 5, 6],
                ['b', 6, 7],
              ['c', 8, 9],
                  ['c', 9, 10],
                  ['d', 2,np.nan ],
                  ['d', 4,3]],
             columns=['A', 'B', 'C'])
#print(df3)
#df3['Total']=df3['B'].apply(lambda x: np.mean(x),axis=0)


