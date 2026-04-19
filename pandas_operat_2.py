import pandas as pd
import numpy as np

# data = {
#     'Column1': [1,2,3,4,5],
#     'Column2': [10,20,20,45,25],
#     'Column3': ["abc1","bc","ade","cba","d22ea"]
# }



# def kareal(x):
#     return x * x

# kare2al = lambda x: x*x
# df = pd.DataFrame(data)
# result = df
# result = df["Column2"].unique()
# result = df["Column2"].nunique()
# result = df["Column2"].value_counts()
# result = df["Column2"]*2
# result = df["Column2"].apply(kareal)
# result = df["Column2"].apply(kare2al)

# print(result)
# result = df["Column3"].apply(len)
# print(result)
# df['Column4'] = result
# print(df[["Column3","Column4"]])
# result = df.sort_values("Column2")
# result = df.sort_values("Column3",ascending=False)
# print(result)
data = {
    "Ay": ["Mayıs","Aralık","Nisan","Mayıs","Haziran","Nisan","Ocak","Haziran","Nisan"],
    "Kategori": ["Elektronik","Elektronik","Elektronik","Kitap","Kitap","Kitap","Giyim","Giyim","Giyim"],
    "Gelir": [20,30,15,14,32,42,12,36,52]
}
df = pd.DataFrame(data) 
df = df.pivot_table(index="Ay", columns="Kategori", values="Gelir")
df = df.sort_values("Ay",ascending=False)




