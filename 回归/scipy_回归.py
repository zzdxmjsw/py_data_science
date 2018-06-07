from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(12345678)
x = np.random.random(10)
y = np.random.random(10)
z = np.random.random(10)
slop,intercept,r_value,p_value,std_err = stats.linregress(x,y)

plt.plot(x,y,'o',label='origin')
plt.plot(x,intercept+slop*x,'r',label='fitted line')

