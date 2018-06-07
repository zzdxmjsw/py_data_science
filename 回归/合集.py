from scipy import linspace, polyval, polyfit, sqrt, stats, randn, optimize
import statsmodels.api as sm
import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# =====生成数据
n = int(5e6)  # 数据量
xi = np.linspace(-10, 10, n)  # x 数据点
x2i = xi**2 -2
# parameters
a = 3.25
b = -6.5
y0 = polyval([a, b], xi)  # -39 to 26, y数据点
# add some noise
yi = y0 + 3 * randn(n)  # 加入噪声


xvar = np.random.choice(xi, size=20)
yvar = polyval([a, b], xvar) + 3 * randn(20)
plt.scatter(xvar, yvar, c='green', edgecolors='k')
plt.grid(True)
plt.show()

# =================scipy.polyfit
t1 = time.time()
(ahat, bhat) = polyfit(xi, yi, 1)  # 两个估计值
yhat = polyval([ahat, bhat], xi)  # 拟合值
# compute the mean square error
err = sqrt(sum((yhat - yi)**2) / n)  # yi-yhat
t2 = time.time()
time_polyfit = float(t2 - t1)

print('Linear regression using polyfit')
print('parameters: a=%.2f b=%.2f, ms error= %.3f' % (ahat, bhat, err))
print("Time taken: {} seconds".format(time_polyfit))

#=================stats.linregression
t1 = time.time()
(a_s, b_s, r, tt, stderr) = stats.linregress(xi, yi)  # 斜率 截距 相关系数 p值 标准差
t2 = time.time()
t_linregress = float(t2 - t1)

print('Linear regression using stats.linregress')
print(
    'a=%.2f b=%.2f, std error= %.3f, r^2 coefficient= %.3f' %
     (a_s, b_s, stderr, r))
print("Time taken: {} seconds".format(t_linregress))


#==================optimize.curve_fit
def flin(t, a, b):
    result = a * t + b
    return(result)


t1 = time.time()
p1, _ = optimize.curve_fit(flin, xdata=xi, ydata=yi, method='lm')  # 估计值 协方差?
t2 = time.time()
t_optimize_curve_fit = float(t2 - t1)

print('Linear regression using optimize.curve_fit')
print('parameters: a=%.2f b=%.2f' % (p1[0], p1[1]))
print("Time taken: {} seconds".format(t_optimize_curve_fit))

#=================numpy.linalg

t1 = time.time()
A = np.vstack([xi, np.ones(len(xi))]).T
result = np.linalg.lstsq(A, yi)
ar, br = result[0]
err = np.sqrt(result[1] / len(yi))
t2 = time.time()
t_linalg_lstsq = float(t2 - t1)

print('Linear regression using numpy.linalg.lstsq')
print('parameters: a=%.2f b=%.2f, ms error= %.3f' % (ar, br, err))
print("Time taken: {} seconds".format(t_linalg_lstsq))

#===================statsmodels
t1 = time.time()
t = sm.add_constant(xi)
model = sm.OLS(y0, t)
results = model.fit()
ar = results.params[1]
br = results.params[0]
t2 = time.time()
t_OLS = float(t2 - t1)

print('Linear regression using statsmodels.OLS')
print('parameters: a=%.2f b=%.2f' % (ar, br))
print("Time taken: {} seconds".format(t_OLS))

print(results.summary())


#====================
