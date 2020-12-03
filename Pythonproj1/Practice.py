import pandas as pd
import timeit
import numpy as np
import re

df=pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]],columns=list('ABC'))
v=list()
v=[7,8,9]
df['C']=v
print(df)

