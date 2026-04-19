
import pandas as pd
import numpy as np
df = pd.read_csv("C:\\users\\exper\\documents\\python_test\\nba.csv")
df = pd.DataFrame(df)
# result = len(df.columns)
# result = df.columns
# result = len(df.index)
# result = df.info
# result = df.head(10)

# # resul = len(df.columns)
# # res = len(df.index)
# # total = resul* res
# resul = df['Salary'].max()
# print()
# result = df[df["Salary"] == df['Salary'].max()] ['Name'].iloc[0]
# print(f"{result} isimli oyuncunun maaşı :{resul} dir.")
#result = df[(df["Age"] >= 20) & (df["Age"]<=25)] [["Name","Team","Age"]].sort_values("Age", ascending=False)
# result = df.sort_values("Team", ascending=False)
#result = df[(df["Name"] == "John Holland")] [["Name","Age","Team"]].iloc[0]
# data ={
#     'Takım':[]
#     'Maas_Ort':[]
# }
# result = df.groupby("Team").size()
# result = df['Team'].value_counts()
df = df.dropna()
# result =  df[df["Name"].str.contains("and")].head(20) ['Name'].iloc[::-1]
def str_find(name):
    if "and" in name.lower():
        return True
    return False
result = df[df["Name"].apply(str_find)]
print(result)