import numpy as np

result = np.array([10,15,30,45,60])
result = np.arange(5,16)
result =np.arange(50,101,5)
result = np.zeros(10)
result =np.ones(10)
result = np.linspace(0,100,5)
result = np.random.randint(10,30,5)
result = np.random.randn(10)

result = np.random.randint(10,50,15).reshape(3,5)
matris = np.random.randint(10,50,15).reshape(3,5)

rowTotal = matris.sum(axis=1)
colTotal =matris.sum(axis=0)
print(matris)
print('satır:')
print(rowTotal)
print('sütun:')
print(colTotal)
top=0
for i in colTotal:
    top += i
print('genel toplam:')
print(top)

result = matris[matris %2!=0]
print(result)
result = result[result>=40]


print(result)



#print(result)