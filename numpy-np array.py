import numpy as np

py_list = [0,1,2,3,4,5,6,7,8,9,10]
#py_list.
np_array = np.array([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
print(type(py_list))
print(type(np_array))
np_multi = np_array.reshape(2,8)
print(py_list)
print(np_array)
print(np_multi)
print(np_array.shape)
print(np_multi.shape)