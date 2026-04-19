import numpy as np

numbers1 = np.random.randint(10,100,6)
 
numbers2 = np.random.randint(10,100,6)
print(numbers1)

print(numbers2)
result = numbers1 + 10

print(result)
result= (numbers1 / 10) *numbers2
print(result)
result = result[::-1]

print(np.sqrt(result))