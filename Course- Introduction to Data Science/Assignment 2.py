import pandas as pd
import numpy as np
import scipy.stats as stats

df=pd.read_csv('datasets/NISPUF17.csv')
#print(df.head())
df1=df[df["EDUC1"]==1]
df2=df[df["EDUC1"]==2]
df3=df[df["EDUC1"]==3]
df4=df[df['EDUC1']==4]
n1=np.sum(df1["EDUC1"].dropna())
n2=np.sum(df2["EDUC1"].dropna())
n3=np.sum(df3["EDUC1"].dropna())
n4=np.sum(df4["EDUC1"].dropna())
val1=n1/(len(df['EDUC1'].dropna()))
val2=n2/(len(df['EDUC1'].dropna()))
val3=n3/(len(df['EDUC1'].dropna()))
val4=n4/(len(df["EDUC1"].dropna()))
#HAD_CPOX
#P_NUMVRC
#print(val1,val2,val3,val4)

##################################


DfM=df.where((df['HAD_CPOX']==1) & (df['P_NUMVRC']>=1) & (df['SEX']==1))
DfM1=df.where((df['HAD_CPOX']==2) & (df['P_NUMVRC']>=1)& (df['SEX']==1))
DfF=df.where((df['HAD_CPOX']==1) & (df['P_NUMVRC']>=1) & (df['SEX']==2))
DfF1=df.where((df['HAD_CPOX']==2) & (df['P_NUMVRC']>=1) & (df['SEX']==2))
mval=len(DfM['HAD_CPOX'].dropna())/len(DfM1['HAD_CPOX'].dropna())
#print(mval)
fval=len(DfF['HAD_CPOX'].dropna())/len(DfF1['HAD_CPOX'].dropna())
#print(fval)

##################################

DF=df.where(((df['HAD_CPOX']==1) | (df['HAD_CPOX']==2)) & (df['P_NUMVRC']>=0))

#print(DF['HAD_CPOX'].dropna())
# here is some stub code to actually run the correlation
corr, pval = stats.pearsonr(DF["HAD_CPOX"].dropna(), DF["P_NUMVRC"].dropna())

# just return the correlation
#print(corr)

#################################
df = pd.read_csv('datasets/NISPUF17.csv')
df1 = df.where((df["CBF_01"] == 1) & (df['P_NUMFLU'] >= 0))
df2 = df.where((df["CBF_01"] == 2) & (df['P_NUMFLU'] >= 0))

pval1 = (np.sum(df1['P_NUMFLU'].dropna())) / (len(df1["P_NUMFLU"].dropna()))
pval2 = (np.sum(df2['P_NUMFLU'].dropna())) / (len(df2["P_NUMFLU"].dropna()))
print(pval1, pval2)

