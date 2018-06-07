import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

'''an = np.linspace(1,10000000, num = 10000000)
bn = 1/an
sn = bn.cumsum()

# p 级数

def p_func(i):
    return 1/i**2

cn = np.fromfunction(p_func,(10000001,))[1:]
dn = cn.cumsum()

def p_func2(i):
    return 1/i**1.000000001

en = np.fromfunction(p_func2,(10000001,))[1:]
fn = en.cumsum()

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)

ax1.plot(sn)
ax2.plot(dn)
ax3.plot(fn)'''


def p_func(i):
    return 3**(-i**0.5)


an = np.fromfunction(p_func, (10000001,))[1:]
bn = an.cumsum()

plt.plot(bn)

import statsmodels