import numpy as np
from scipy.optimize import leastsq
import pylab as pl


def func(x, p):  # p为列表
    """
    数据拟合所用的函数: A*sin(2*pi*k*x + theta)
    """
    A, k, theta = p
    return A * np.sin(2 * np.pi * k * x + theta)


def residuals(p, y, x):
    """
    实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
    """
    return y - func(x, p)


x = np.linspace(0, -2 * np.pi, 100)
A, k, theta = 10, 0.34, np.pi / 6  # 真实数据的函数参数
y0 = func(x, [A, k, theta])  # 真实数据
y1 = y0 + 2 * np.random.randn(len(x))  # 加入噪声之后的实验数据

p0 = [20, 0.2, 0]  # 第一次猜测的函数拟合参数

# 调用leastsq进行数据拟合
# residuals为计算误差的函数
# p0为拟合参数的初始值
# args为需要拟合的实验数据
seq = leastsq(residuals, p0, args=(y1, x))  # y1 和 x 表示实际中可能遇到的带噪音的数据

print("真实参数:", [A, k, theta])
print("拟合参数", seq[0])  # 实验数据拟合后的参数

pl.plot(x, y0, label="real para")
pl.plot(x, y1, label="noisy para")
pl.plot(x, func(x, seq[0]), label="simulate para")
pl.legend()
pl.show()
