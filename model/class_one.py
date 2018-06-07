import numpy as np
import matplotlib.pyplot as plt
mass = [50 * i for i in range(1, 12)]  # 这里偷懒用的列表推导式，python初学者可以百度一下，一看就懂
length = [
    1.000,
    1.875,
    2.750,
    3.250,
    4.375,
    4.875,
    5.675,
    6.500,
    7.250,
    8.000,
    8.750]
reg = np.polyfit(mass, length, deg=1)  # 按一次多项式拟合
# print(reg)  # 输出各项系数

P = np.poly1d(reg)
# print(P)  # 输出方程式

length_sim = np.polyval(reg, x=mass)
# print(length_sim)

plt.scatter(mass, length, label='origin')
plt.plot(mass, length_sim, 'r-', label='regression')
