import numpy as np
import matplotlib.pyplot as plt
import seaborn

ar = np.random.normal(0,1,50)
ar_cum = ar.cumsum()

seaborn.kdeplot(ar)
plt.show()

plt.plot(ar_cum)
plt.show()