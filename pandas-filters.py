import pandas as pd
import numpy as np

data = np.random.randint(10,100,75).reshape(15,5)
df = pd.DataFrame(data, columns=["column1","column2","column3","column4","column5"])

result = df
result = df.columns
result = df.head(5)
result = df.tail(3)
result = df['column2'].head(1)
result = df.column2.head(2)
result = df[["column2","column1"]].head(1)
result = df[["column2","column1"]].tail(1)
result = df[5:11] [["column2","column1"]].tail(3)
result = df >= 50
result = df[(df["column2"]>=50) & (df["column1"]<=70)][["column1","column2"]]
result = df.query("column1 >=50 & column2 % 2 == 0 & column3 >=50 & column4 % 2 == 0")

print(result)