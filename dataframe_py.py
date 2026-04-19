import pandas as pd
import numpy as np


# s1 = pd.Series([3,2,0,1])
# s2 = pd.Series([0,3,7,2])

# data = dict(apples =s1, oranges =s2)
# df = pd.DataFrame(data)
# print(df)
df = pd.DataFrame()
df = pd.DataFrame([1,2,3,4])
list = [["ahmet",50],["ali",60],["yağmur",70],["çınar",80]]
dict ={'name':["Ahmet","erdal","hasan","murat"],'grade':[50,60,70,80]}

df = pd.DataFrame(list, columns=['Name','Grade'], index=[1,2,3,4])
df = pd.DataFrame(list, columns=['Name','Grade'], dtype=float)
df = pd.DataFrame(dict,index=[212,512,445,217])


print(df)
