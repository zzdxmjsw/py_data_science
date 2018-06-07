import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.random.random(50000)
y = np.random.random(50000)
boolean = np.ones(50000)

plot_data = np.array([x, y, boolean]).T

'''for i in plot_data:
    if i[0]**2 + i[1]**2 > 1:
        i[2] = 0'''
# ==向量化：
idx = plot_data[:,0]**2+plot_data[:,1]**2<1
plot_data[idx,2] = 0


plot_data = pd.DataFrame(plot_data, columns=['x', 'y', 'boolean'])

#  区分内外点
in_df = plot_data[plot_data['boolean'] == 1]
out_df = plot_data[plot_data['boolean'] == 0]

a = plt.plot(in_df['x'], in_df['y'], '.')[0]
plt.setp(a, markersize=0.3)
b = plt.plot(out_df['x'], out_df['y'], '.')[0]
plt.setp(b, markersize=0.3)
print('pi值模拟结果为' + str(len(in_df) / len(x) * 4))
# 更多参数见http://matplotlib.org/users/pyplot_tutorial.html
