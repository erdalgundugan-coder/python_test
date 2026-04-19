import pandas as pd
import numpy as np

personeller = {
    'Çalışan': ['Ahmet Yılmaz','Can Ertürk','Hasan Korkmaz','Cenk Saymaz','Ali Turan','Rıza Ertürk','Mustafa Can'],
    'Departman':['İnsan Kaynakları','Bilgi İşlem','Muhasebe','İnsan Kaynakları','Bilgi İşlem','Muhasebe','İnsan Kaynakları'],
    'Yaş':[30,25,45,50,23,24,42],
    'Semt':['Kadıköy','Tuzla','Maltepe','Tuzla','Maltepe','Tuzla','Kadıköy'],
    'Maaş':[5000,3000,4000,3500,2750,6500,4500]
}

df = pd.DataFrame(personeller)
result = df["Maaş"].sum()
result = df.groupby("Departman").groups
result = df.groupby(["Departman","Semt"]).groups
# semtler = df.groupby("Semt")
# for name,group in semtler:
#     print(name)
#     print(group)
# for name,group in df.groupby("Departman"):
#     print(name)
#     print(group)
# print()
result = df.groupby("Departman").get_group("Muhasebe")
result = df.groupby("Departman").sum()
result = df.groupby("Departman")["Maaş"].mean()
result = df.groupby("Semt")["Çalışan"].count()
result = df.groupby("Departman").mean()
print(result)
