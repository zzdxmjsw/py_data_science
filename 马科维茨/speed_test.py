from numba import jit
from numpy import arange
from datetime import datetime

# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.


@jit
def sum2d(arr):
    m, n = arr.shape
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += arr[i, j]
    return result


a = arange(999999999).reshape(111111111, 9)
start = datetime.now()
print(sum2d(a))
stop = datetime.now()
print(stop-start)
