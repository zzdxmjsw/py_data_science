import pandas as pd
import json
import matplotlib
import numpy as np
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt
import tushare as ts
import scipy.optimize as sco
import numexpr as ne
from numba import jit


def get_lager_one(df_a, df_b):
    if len(df_a) > len(df_b):
        return 'left'
    else:
        return 'right'


# f = open('code_name.json', encoding='utf-8')
# text = f.read()
# d = json.loads(text)


stock_set = ['000413', '000725', '600798', '600549', '600111']
noa = len(stock_set)
df = []
for i in range(noa):
    if i == 0:
        df = ts.get_k_data(
            stock_set[i], start='2015-01-01', end='2017-09-24')[['date', 'close']]
        # df.columns = ['date', d[stock_set[i]]]
        df.columns = ['date', stock_set[i]]
    else:
        df_single = ts.get_k_data(
            stock_set[i], start='2015-01-01', end='2017-09-24')[['date', 'close']]
        # df_single.columns = ['date', d[stock_set[i]]]
        df_single.columns = ['date', stock_set[i]]
        df = pd.merge(left=df, right=df_single, on='date')


df_final = df.iloc[:, 1:]
df_final.index = df.iloc[:, 0]  # 原始数据

df_final = df_final / df_final.iloc[0] * 100  # 忽略个股差异，在开始时间上都以100为起点
''''# ==========绘图+中文============
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

df_final.plot()'''

# 用对数回报率可以将回报率简单相加而不用相乘，因此可乘以252表全年
returns = np.log(df_final / df_final.shift(1))
# print(returns*252)
cov = returns.cov() * 252

#  =======分配权重========
weight = np.random.random(noa)  # 生成指定个数的随机数
weight /= np.sum(weight)  # 将组合权重之和确定为1

porto_return = np.sum(returns.mean() * weight) * 252  # 组合回报率
porto_var = np.dot(weight.T, np.dot(cov, weight))
std = np.sqrt(porto_var)


# ========Monte Carlo=======
def monte_carlo(num):
    port_returns = []
    port_variance = []

    for p in range(num):
        weights = np.random.random(noa)
        weights /= np.sum(weights)
        port_returns.append(np.sum(returns.mean() * 252 * weights))
        port_variance.append(np.sqrt(
            np.dot(
                weights.T,
                np.dot(
                    returns.cov() *
                    252,
                    weights))))
    port_returns = np.array(port_returns)
    port_variance = np.array(port_variance)
    print('循环结束')
    # 无风险利率设定为4%
    risk_free = 0.04
    plt.figure(figsize=(12, 8))
    plt.scatter(port_variance, port_returns, c=(
        port_returns - risk_free) / port_variance, marker='o')
    plt.grid(True)
    plt.xlabel('excepted volatility')
    plt.ylabel('expected return')
    plt.colorbar(label='Sharpe ratio')


# ===========最小夏普比率=============
def statistics(weights):
    weights = np.array(weights)
    port_returns = np.sum(returns.mean() * weights) * 252
    port_variance = np.sqrt(
        np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return np.array([port_returns, port_variance,
                     port_returns / port_variance])


# 最优化投资组合的推导是一个约束最优化问题

# 最小化夏普指数的负值


def min_sharpe(weights):
    return -1 * statistics(weights)[2]


# 约束是所有参数(权重)的总和为1。这可以用minimize函数的约定表达如下
cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# 我们还将参数值(权重)限制在0和1之间。这些值以多个元组组成的一个元组形式提供给最小化函数
bnds = tuple((0, 1) for x in range(noa))

# 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。我们简单的使用平均分布。
opts = sco.minimize(min_sharpe, noa * [1. / noa, ],
                    method='SLSQP',
                    bounds=bnds,
                    constraints=cons)

# ===========最小方差===============


def min_variance(weights):
    return statistics(weights)[1]


optv = sco.minimize(min_variance,
                    noa * [1. / noa,
                           ],
                    method='SLSQP',
                    bounds=bnds,
                    constraints=cons)


# ===========有效前沿==============
def min_variance(weights):
    return statistics(weights)[1]


# 在不同目标收益率水平（target_returns）循环时，最小化的一个约束条件会变化。
target_returns = np.linspace(0.0, 0.5, 50)
target_variance = []
for tar in target_returns:
    cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[
            0] - tar}, {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    res = sco.minimize(min_variance,
                       noa * [1. / noa,
                              ],
                       method='SLSQP',
                       bounds=bnds,
                       constraints=cons)
    target_variance.append(res['fun'])

target_variance = np.array(target_variance)
