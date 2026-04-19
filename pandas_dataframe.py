import pandas as pd
from numpy.random import randn
df = pd.DataFrame(randn(3,3),index=["A","B","C"], columns=["columns1","columns2","columns3"])
print(df)
result =df
result = df[["columns1","columns3"]]
print()
result = type(df.loc['A'])

result = df.loc[:,"columns2"]
result = df.loc[:,['columns3',"columns2"]]
result = df.loc['B',['columns1', "columns2"]]
result = df.loc['C',:"columns3"]
result = df.loc[['A','B'],['columns1', "columns2"]]
df["columns4"] = pd.Series(randn(3),["A","B","C"])
df["columns5"] = df["columns1"]+df["columns3"]
print(df.drop("columns1", axis=1))
print(df)
print(result)

