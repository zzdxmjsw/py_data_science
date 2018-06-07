import theano as th
import numpy as np

m1 = np.random.random([10000,3000]).astype(np.float32)
m2 = np.random.random([3000,10000]).astype(np.float32)


a = th.tensor.matrix()  # 定义变量类型
b = th.tensor.matrix()
c = th.dot(a,b)
func = th.function([a,b],c)
