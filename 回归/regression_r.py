import numpy as np
import scipy
import statsmodels.api as sm
# Polynomial Regression
import matplotlib.pyplot as plt


def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

    # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y) / len(y)          # or sum(y)/len(y)
    # or sum([ (yihat - ybar)**2 for yihat in yhat])
    ssreg = np.sum((yhat - ybar)**2)
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results


nsample = 100
x = np.linspace(0, 10, nsample)  # 0-10 包含头尾的100个值 10/99
_x = sm.add_constant(x)  # 100行2列,第一列为1
beta = np.array([1, 10])  # 2行1列
e = np.random.normal(size=nsample)
# y 在矩阵乘法后变为100行的array,每个数为x*10+1+噪声-----按y=10x+1模拟出带噪声的数据组
y = np.dot(_x, beta) + e

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
y_hat = np.dot(_x, np.array([intercept, slope]))

plt.plot(x, y, 'r-', label='origin')
plt.plot(x, y_hat, 'b-', label='fitted')
plt.legend(loc='upper left')
plt.annotate('R^2 = %s' % r_value, (1, 80))
