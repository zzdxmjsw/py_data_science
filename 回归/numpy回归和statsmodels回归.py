import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 一元线性回归
nsample = 100
x = np.linspace(0, 10, nsample)  # 0-10 包含头尾的100个值 10/99
_x = sm.add_constant(x)  # 100行2列,第一列为1
beta = np.array([1, 10])  # 2行1列
e = np.random.normal(size=nsample)
# y 在矩阵乘法后变为100行的array,每个数为x*10+1+噪声-----按y=10x+1模拟出带噪声的数据组
y = np.dot(_x, beta) + e
# 实际上就是对x的变化，与_x无关

model = sm.OLS(y, _x)  # 先endog(因变量、反应变量),后exog(自变量、回归变量)
results = model.fit()

y_fitted = results.fittedvalues  # 回归曲线上的值，但没有此函数的代码补全
plt.plot(x, y)  # 绘图时要按x的坐标轴
plt.plot(x, y_fitted)

# 一元高次回归
nsample = 100
x = np.linspace(0, 10, nsample)
_x = np.column_stack((x, x**2))  # 100行2列,第一列为x，第二列为x**2
_x = sm.add_constant(_x)  # 100行3列,第一列为1，后两列为原_x
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=nsample)
y = np.dot(_x, beta) + e  # 按y=1+0.1x+10x**2 模拟出的数组
model = sm.OLS(y, _x)
results = model.fit()
y_fitted = results.fittedvalues
plt.plot(x, y, 'o')
plt.plot(x, y_fitted, 'r-')

# 一元线性回归 numpy法


def f(x_para):
    return np.sin(x_para) + 0.5 * x_para


x = np.linspace(-2 * np.pi, 2 * np.pi, 50)
y = f(x)
reg = np.polyfit(x, y, deg=1)  # deg控制回归的次数,且默认基为全1矩阵
ry = np.polyval(reg, x)
plt.plot(x, y, 'b')
plt.plot(x, ry, 'r.')

# 一元高次回归 numpy法
reg = np.polyfit(x, y, deg=5)
ry = np.polyval(reg, x)
plt.plot(x, y, 'b')
plt.plot(x, ry, 'r.')

# 一元可变基高次回归 numpy-lstsq法
basic_matrix = np.zeros((4, len(x)))  # 假设为3次回归，需要4个参数，生成4行50列的数组
basic_matrix[3, :] = x**3
basic_matrix[2, :] = x**2
basic_matrix[1, :] = x
basic_matrix[0, :] = 1  # 化成x^3,x^2,x,1组成的矩阵为基
reg = np.linalg.lstsq(basic_matrix.T, y)[0]  # 以基和结果矩阵为参数，求出由基导出结果矩阵的系数
ry = np.dot(reg.T, basic_matrix)  # 1行4列乘4行50列
plt.plot(x, y, 'b')
plt.plot(x, ry, 'r.')
# 换成含sin的基

basic_matrix[3, :] = np.sin(x)
reg = np.linalg.lstsq(basic_matrix.T, y)[0]
ry = np.dot(reg.T, basic_matrix)
plt.plot(x, y, 'b')
plt.plot(x, ry, 'r.')
