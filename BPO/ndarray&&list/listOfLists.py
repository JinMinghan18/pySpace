import numpy as np
examGrads=[
    [79, 95, 60],
    [95, 60, 61],
    [99, 67, 84],
    [76, 76, 97],
    [91, 84, 98],
    [70, 69, 96],
    [88, 65, 76],
    [67, 73, 80],
    [82, 89, 61],
    [94, 67, 88]]

# print(examGrads[2])
gArray = np.array(examGrads)
# print(gArray[0,2])
# print(gArray[2,:])
# print(gArray[:,0])
# print(gArray[:3,:2])
#
# tarray = np.eye(3)
# tarray2 = np.zeros((2,3))
# print(tarray)
# print(tarray2)
# print(gArray[[1,3]][0,[0,2]])

# arr = gArray
# print(arr is gArray)
#
# v = np.array([48,6,51,32,4,85])
# print(v)
#
# print(v.dtype)
# print(v.shape)
#
# v = v.astype(np.float32)
# print(v.dtype)
# print(v.shape)
#
# print(sum(v[0:3]))
# print(np.average(v[-1:-5:-1]**2))
#
# print(max(v),min(v))
# v = list(v)
# print(v.index(max(v)),v.index(min(v)))
#
# print("排序前的索引",np.argsort(v))
# print("排序后的向量",np.sort(v))
#

marray = np.array([
    [45  ,62  ,31  ,753 ],
    [78  ,43  ,12  ,546 ],
    [146 ,785 ,2475,7   ]
])
print(marray)
print(type(marray))
print(marray.dtype)
print(marray.shape)
m = marray.astype(np.float32)
print(m.dtype)
print(m.shape)

m = m.T
print(m)

print(m.sum(axis=0))
print(m.sum(axis=1))

print(np.sqrt(sum(np.square(m[0,:]-m[1,:]))))
print(np.linalg.norm((m[0,:] - m[1,:])))
y = np.linalg.norm(m,axis=1,keepdims=True)
z = m/y
print(z)

print(sum(m/m.sum(axis=0)))
# print(sum(m/m.sum(axis=1)))

h = z.T
c = z.dot(h)
print(c)