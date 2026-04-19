import pandas as pd
df = pd.read_csv("C:\\users\\exper\\documents\\python_test\\IMDB_Bottom250.csv")

# result = df.columns
# print(result)
# result = df[df["Year"] >= 2015] [["Year","Title","Actors"]]
# print(result)

# result = df.iloc[10] [["Year","Title","Actors"]]

# result = df.info
# print(result)
#result = df
result = df[df["Country"] =="Turkey"]  [["Year","Title","Director","Actors"]].head(500)

print(result)