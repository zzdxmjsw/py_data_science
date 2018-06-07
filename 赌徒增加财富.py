import random
import numpy as np
import pandas as pd
from numba import jit


ar = np.arange(1,5001)
df = pd.DataFrame(ar)

@jit
def operation(times):
    num = 0
    for i in range(times):
        if num == 0:
            rand = 1
        elif num == 2:
            rand = -1
        else:
            rand = random.choice([-1,1])
        num += rand
    return num

df['result'] = df.apply(lambda row:operation(row[0]),axis=1)
# todo 改进算法++


