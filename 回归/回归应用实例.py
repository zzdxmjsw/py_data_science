import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
shh = ts.get_hist_data(code='sh', start='2017-01-01', end='2017-08-11')
sz = ts.get_hist_data(code='sz', start='2017-01-01', end='2017-08-11')

shh_pct = shh['p_change']
sz_pct = sz['p_change']
# 防止两市成交天数不一
if len(shh_pct) > len(sz_pct):
    shh_pct = shh_pct[sz_pct.index]
else:
    sz_pct = sz_pct[shh_pct.index]

reg = np.polyfit(shh_pct, sz_pct, deg=1)
ry = np.polyval(reg, shh_pct)
plt.plot(shh_pct, sz_pct, 'r.')
plt.plot(shh_pct, ry, 'b')
