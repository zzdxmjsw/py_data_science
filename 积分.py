import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import integrate


def f(x):
    return np.sin(x) + 0.5 * x


a = 0.5
b = 9.5
x = np.linspace(0, 10)
y = f(x)
# 求积分方法
integrate.fixed_quad(f, a, b)  # 固定高斯求积

integrate.quad(f, a, b)  # 自适应求积

xi = np.linspace(0.5, 9.5, 100)
integrate.trapz(f(xi), xi)  # 梯形法则

integrate.simps(f(xi), xi)  # 辛普森法则
np.random.normal(size=20)

# 正态随机范例
x = sorted(np.random.normal(loc=5, scale=10, size=2000))
plt.hist(x, bins=100)

# 通过模拟求积分
np.random.seed(1000)  # 设置种子数
x = np.random.random(2000) * (b - a) + a  # 将x的值设置为区间范围内的一个随机数
np.sum(f(x)) / len(x) * (b - a)  # 先求出积分区间的平均函数值，再乘以区间长度得出积分值
